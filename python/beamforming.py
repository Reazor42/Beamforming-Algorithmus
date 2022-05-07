import PyQt5.QtCore
import acoular
import matplotlib.pyplot as plt
from PIL import ImageSequence
from PIL import Image
from celluloid import Camera
import os
import scipy.io.wavfile as wavf
from tqdm import tqdm
import numpy as np
import h5py


def removeWhitePixels(gifpath):
    # using PIL
    img = Image.open(gifpath)
    images = []

    frames = ImageSequence.Iterator(img)

    for frame in frames:

        try:
            img_mod = frame.convert("RGBA")
            datas = img_mod.getdata()

            newData = []
            # Currently only peaks stored but rest of the plot is white, so remove white pixels
            for item in datas:
                if item[0] == 0 and item[1] == 0 and item[2] == 0:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)

            img_mod.putdata(newData)

            images.append(img_mod)

        except EOFError:
            continue

    path = os.path.dirname(gifpath) + "/gifoverlay.gif"
    # hier gucken
    images[0].save(path, save_all=True, append_images=images[1:], optimize=True, duration=gif_interval, loop=0,
                   disposal=2,
                   transparency=0)

    return path


# Diese Daten hier verändern!


audio_file = "data/data_1/Audio1_4m_40db.wav"  # name if .h5 audio data
video_data = "data/data_1/Video1_4m_40db.mp4"  # name of the video
mic_config = "config/mic32.xml"  # path of mic configuration
z_distance = 3  # Kind of the distance to the audio source (kind of)
resolution = 0.1  # the smaller, the sharper
frequency = 550  # band center frequency in hz
samples_per_image = 48000 // 1  # 48000 = 1 Second
x_min = -3
x_max = 3
y_min = -1.5
y_max = 1.5
gif_interval = 1000 / 1
interval = 1 / 1


def get_acoular_essentials():
    # Set the mic array geometry
    mg = acoular.MicGeom(from_file="config/mic32.xml")

    rg = acoular.RectGrid(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                          z=z_distance,
                          increment=resolution)

    st = acoular.SteeringVector(grid=rg, mics=mg)

    return mg, rg, st


def do_beamforming(mic_data, endtime):
    """ Beamforming using Acoular """
    mg, rg, st = get_acoular_essentials()

    count = 0
    # Divide audio samples as per frame rate (10fps) and do beamforming
    for s_time in tqdm(np.arange(0, endtime, interval)):

        audio_data = mic_data[:, int(s_time * samples_per_image): int((s_time + interval) * samples_per_image)]
        audio_data = np.transpose(audio_data)

        if audio_data.shape[0] == 0:
            continue

        # Acoular needs audio input through .h5 file
        target_file = 'img/temp.h5'

        if os.path.exists(target_file):
            os.remove(target_file)

        with h5py.File(target_file, 'w') as data_file:
            data_file.create_dataset('time_data', data=audio_data)
            data_file['time_data'].attrs.__setitem__('sample_freq', samples_per_image)

        # .h5 file has issues with closing. Change 'ulimit' if not working

        ts = acoular.TimeSamples(name=target_file)
        ps = acoular.PowerSpectra(time_data=ts, block_size=128, window='Hanning', overlap='50%')
        bb = acoular.BeamformerEig(freq_data=ps, steer=st)

        pm = bb.synthetic(frequency, 4)
        Lm = acoular.L_p(pm)

        if count == 0:
            bf_data = np.zeros(
                (Lm.shape[0], Lm.shape[1], len(np.arange(0, endtime, interval))))
            bf_data[:, :, count] = Lm
        else:
            bf_data[:, :, count] = Lm

        count += 1

    # remove temp.h5 file after its finished
    os.remove(target_file)

    return bf_data, rg


def savePlot(bf_data, rg):
    print("Saving plot.........")
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)
    camera = Camera(fig)

    for i in range(0, bf_data.shape[2]):
        """
        setting of minimum (plot_min) is arbitrary and 
        is set by looping through all the frames and guessing a number
        """
        plot_min = bf_data[:, :, i].max() - 10
        plot_max = bf_data[:, :, i].max()

        # plot result
        im = ax.imshow(bf_data[:, :, i].T, cmap='plasma', origin='lower', vmin=plot_min, vmax=plot_max,
                       extent=rg.extend(), interpolation='bicubic')

        max_bf_data = bf_data[:, :, i].max()

        ax.set_aspect('equal')
        for axi in (ax.xaxis, ax.yaxis):
            for tic in axi.get_major_ticks():
                tic.tick1line.set_visible(False)
                tic.tick2line.set_visible(False)
                tic.label1.set_visible(False)
                tic.label2.set_visible(False)

        fig.tight_layout(pad=0)

        # save plot to create .gif
        camera.snap()

    animation = camera.animate(interval=gif_interval, blit=True)

    gif_name = 'vid.gif'

    # decide where to store the file (base self.outfile)

    output_dir = "img/"

    gif_path = output_dir + gif_name

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # save .gif
    animation.save(gif_path, writer='imagemagick')
    plt.close('all')

    return gif_path


sample_rate, md = wavf.read(audio_file)
endtime = md.shape[0]/sample_rate
arg, bf_data = do_beamforming(md, endtime)
gif_name = savePlot(bf_data, arg)
gif_path = removeWhitePixels(gif_name)

os.system(
    'ffmpeg -hide_banner -loglevel panic -i {0} -i {1} -filter_complex "[1]format=argb,colorchannelmixer=aa=0.4[front];[front]scale=2230:1216[next];[0][next]overlay=x=-155:y=0,format=yuv420p" {2}'.format(
        video_data, gif_path, "overlay.mp4"))

print("Done.")
