# import the necessary modules
import glob
from scipy.io import wavfile
import numpy as np
import tables

import PyQt5.QtCore  # This is needed in some linux systems to work
import acoular
import matplotlib.pyplot as plt
from PIL import ImageSequence
from PIL import Image
from celluloid import Camera
import os
import argparse
from Config import Config
from os.path import join
from tqdm import tqdm


# ======================================================================================================


def merge_waves(path: str) -> str:
    """
    Merges the different WAV-Files into one WAV-File with multiple channels. The resulting WAV-File is named 'merged.wav'

    :param path: Directory with the WAV-Files.
    :return: name of the new multichannel WAV-File (currently merged.wav)
    """
    # find all wav files in the given path
    # then sort the list by length in descending order
    # this puts the files 1-32 in the correct order because the first microphone recordings are a bit shorter than the last ones
    wav_list = glob.glob(join(path, "*.wav"))
    wav_list.sort(key=len)

    # read the wav files and store the sound data (which are numpy arrays) of each file in sound_data_list
    sound_data_list = []
    for f in wav_list:
        samplerate, data = wavfile.read(f)
        sound_data_list.append(data)

    # since the length of the sound data arrays is slightly different, they must be cut to the same length
    # therefore the length of all arrays is read and stored in data_lengths:
    data_lengths = []
    for d in sound_data_list:
        data_lengths.append(len(d))

    # then the length of each array is cut to the minimum length found
    minimum_length = min(data_lengths)
    for i in range(len(sound_data_list)):
        data = sound_data_list[i]
        new_data = data[:minimum_length]
        sound_data_list[i] = new_data

    # put all data arrays from the sound_data_list together in one 2D-numpy array
    # as a result there is an array of shape (32, number_of_samples)
    sound_data_array = np.array(sound_data_list[0])
    for i in range(1, len(sound_data_list)):
        sound_data_array = np.vstack((sound_data_array, sound_data_list[i]))

    # since the array must have the shape (number_of_samples, 32) the array must be transposed
    sound_data_array = sound_data_array.T

    # create the new wav file that contains the new sound_data_array
    file_name = "merged.wav"
    wavfile.write(file_name, 48000, sound_data_array)

    return file_name


# ======================================================================================================

def wav2h5(wav_file: str) -> str:
    """
    Converts a given wav with multiple channels into a hdf5 file so that acoular can process the audio data

    :param wav_file: multichannel wav file
    :return: name of the resulting hdf5 file (currently 'sound_data.h5')
    """
    # define the name of the h5 file to be written
    h5 = "sound_data.h5"

    # read data from wav
    fs, data = wavfile.read(wav_file)

    folder = ''
    # save_to acoular h5 format
    # code was provided in an issue in the acoular github repository: https://github.com/acoular/acoular/issues/25
    acoularh5 = tables.open_file(folder + h5, mode="w", title="test")
    acoularh5.create_earray('/', 'time_data', atom=None, title='', filters=None,
                            expectedrows=100000, chunkshape=[256, 64],
                            byteorder=None, createparents=False, obj=data)
    acoularh5.set_node_attr('/time_data', 'sample_freq', fs)
    acoularh5.close()
    os.remove(wav_file)

    return h5


# ======================================================================================================

def remove_dark_background(gif_path: str, gif_interval: float, processed_gif_path: str) -> None:
    """
    Removes the dark background pixels of the gif image.

    :param gif_path: path to the unprocessed gif file
    :param gif_interval: the fps for the processed gif file (should correspond with the fps of the beamforming)
    :param processed_gif_path: path where the processed gif file should be saved
    """
    img = Image.open(gif_path)
    images = []

    # iterating over all frames of the gif file
    frames = ImageSequence.Iterator(img)
    for frame in frames:

        try:
            img_mod = frame.convert("RGBA")
            datas = img_mod.getdata()

            new_data = []
            # Iterating over every pixel of the frame
            for item in datas:
                # check if pixel is black RGB(0, 0, 0)
                if item[0] == 0 and item[1] == 0 and item[2] == 0:
                    # replace with transparent pixel
                    new_data.append((255, 255, 255, 0))
                else:
                    # replace with same value
                    new_data.append(item)

            img_mod.putdata(new_data)

            # put all new frames into a list
            images.append(img_mod)

        except EOFError:
            continue

    # convert the list into the processed gif file
    images[0].save(processed_gif_path, save_all=True, append_images=images[1:], optimize=True, duration=gif_interval,
                   loop=0,
                   disposal=2,
                   transparency=0)


# ======================================================================================================


def beamforming(h5_file, config: Config) -> None:
    """
    Does the beamforming. Reads the parameters out of the config and generates the acoustic map out of it.
    It will generate a .mp4 video file once it finished which shows the acoustic map merged with the provided video.

    :param h5_file:the path to the hdf5-File
    :param config: an instance of the Config class
    """
    # Stage 1
    mic_config: str = config.array  # path of mic configurationich
    z_distance: int = config.distance  # Kind of the distance to the audio source (kind of)
    resolution: float = config.resolution  # the smaller, the sharper
    frequency: int = config.frequency  # band center frequency in hz
    samples_per_image: int = 48000 // config.fps  # 48000 = 1 Second
    x_min: float = config.x_min
    x_max: float = config.x_max
    y_min: float = config.y_min
    y_max: float = config.y_max
    gif_interval: float = 1000 / config.fps
    audio_data: str = h5_file
    video_data: str = config.video
    out_dir: str = config.output
    transparency: float = config.transparency
    minimum_volume: float = config.minimum_volume

    # Stage 2
    ts: acoular.TimeSamples = acoular.TimeSamples(name=audio_data)
    mg: acoular.MicGeom = acoular.MicGeom(from_file=mic_config)
    print(
        f'Using audio with: {ts.numchannels} channels; {ts.numsamples} samples and a sample frequency of {ts.sample_freq} Hz')
    rg: acoular.RectGrid = acoular.RectGrid(x_min=x_min, x_max=x_max,
                                            y_min=y_min, y_max=y_max,
                                            z=z_distance, increment=resolution)
    st: acoular.SteeringVector = acoular.SteeringVector(grid=rg, mics=mg)

    bt: acoular.BeamformerTime = acoular.BeamformerTime(source=ts, steer=st)
    ft: acoular.FiltOctave = acoular.FiltOctave(source=bt, band=frequency, fraction='Third octave')
    pt: acoular.TimePower = acoular.TimePower(source=ft)
    avgt: acoular.TimeAverage = acoular.TimeAverage(source=pt, naverage=samples_per_image)

    # Stage 3
    fig = plt.figure(figsize=(10, 7))
    cam: Camera = Camera(fig)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    for axi in (ax.xaxis, ax.yaxis):
        for tic in axi.get_major_ticks():
            tic.tick1line.set_visible(False)
            tic.tick2line.set_visible(False)
            tic.label1.set_visible(False)
            tic.label2.set_visible(False)

    fig.tight_layout(pad=0)
    # Stage 4
    number_of_total_frames: int = ts.numsamples // samples_per_image
    for a in tqdm(avgt.result(1), desc="Computing images: ", total=number_of_total_frames, unit="images"):
        r = a.copy()
        pm = r[0].reshape(rg.shape)
        lm = acoular.L_p(pm)
        plt.axis("off")
        ax.imshow(lm.T, vmin=lm.max() - minimum_volume, vmax=lm.max(), origin='lower', cmap='plasma',
                  extent=rg.extend(),
                  interpolation="bicubic")
        cam.snap()
    print("Calculation done... merging to gif")
    unprocessed_gif_path: str = join(out_dir, "vid.gif")
    processed_gif_path: str = join(out_dir, "gifoverlay.gif")

    animation = cam.animate(blit=True, repeat=False, interval=gif_interval)
    animation.save(unprocessed_gif_path, writer='imagemagick')
    # Stage 5
    remove_dark_background(unprocessed_gif_path, gif_interval, processed_gif_path)
    # Stage 6
    os.system(
        f'ffmpeg -hide_banner -loglevel panic -i {video_data} -i {processed_gif_path} -filter_complex "[1]format=argb,colorchannelmixer=aa={transparency}[front];[front]scale=2230:1216[next];[0][next]overlay=x=-155:y=0,format=yuv420p" {join(out_dir, "overlay.mp4")}')
    # removing temporary files
    os.remove(unprocessed_gif_path)
    os.remove(processed_gif_path)
    print("Done.")


def show_microphone_array(mg: acoular.MicGeom) -> None:
    """
    Opens a matplotlib graph which visualises the current numbered microphone arrangement.
    This function is currently not used in the code. It was used for testing purposes.

    :param mg: The microphone array configuration of acoular
    """
    plt.plot(mg.mpos[0], mg.mpos[1], 'o', )
    plt.axis('equal')
    for i in range(len(mg.mpos[0])):
        plt.text(mg.mpos[0][i], mg.mpos[1][i], str(i))
    plt.show()


def parse_arguments() -> argparse.Namespace:
    """
    Reads and sets the command line parameters from the command line.

    :return: argparse.Namespace: Object with the provided command line parameters
    """
    parser = argparse.ArgumentParser(description='Beamforming script for the acoustic camera')
    parser.add_argument("--audio", "-a", default=None)
    parser.add_argument("--video", "-v", default=None)
    parser.add_argument("--array", "-c", default=None)
    parser.add_argument("--distance", "-d", default=3, type=float)
    parser.add_argument("--frequency", "-f", default=550, type=int)
    parser.add_argument("--output", "-o", default=".")
    parser.add_argument("--fps", default=10, type=int)
    parser.add_argument("--resolution", default=0.5, type=float)
    parser.add_argument("--file", default=None)
    parser.add_argument("--x-min", default=-3, type=float)
    parser.add_argument("--x-max", default=3, type=float)
    parser.add_argument("--y-min", default=-2.1, type=float)
    parser.add_argument("--y-max", default=2.1, type=float)
    parser.add_argument("--transparency", default=0.8, type=float)
    parser.add_argument("--min-volume", default=3.0, type=float)
    return parser.parse_args()
