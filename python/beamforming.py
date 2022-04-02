import math

import acoular
import matplotlib.pyplot as plt
from PIL import ImageSequence
from PIL import Image
from celluloid import Camera
import os


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
    images[0].save(path, save_all=True, append_images=images[1:], optimize=True, duration=100, loop=0, disposal=2,
                   transparency=0)

    return path


# Diese Daten hier verändern!


audio_data = "data/test4m.h5"  # name if .h5 audio data
mic_config = "config/mic32.xml"  # path of mic configuration
z_distance = 3  # Kind of the distance to the audio source (kind of)
resolution = 0.1  # the smaller, the sharper
frequency = 550  # band center frequency in hz
samples_per_image = 1600  # 48000 = 1 Second
x_min = -3
x_max = 3
y_min = -1.5
y_max = 1.5

ts = acoular.TimeSamples(name=audio_data)
mg = acoular.MicGeom(from_file=mic_config)
print(
    f'Bearbeite Audio mit: {ts.numchannels} Channeln; {ts.numsamples} Samples und einer Sample-Frequenz von {ts.sample_freq}Hz')
rg = acoular.RectGrid(x_min=x_min, x_max=x_max,
                      y_min=y_min, y_max=y_max,
                      z=z_distance, increment=resolution)
st = acoular.SteeringVector(grid=rg, mics=mg)

bt = acoular.BeamformerTime(source=ts, steer=st)
ft = acoular.FiltOctave(source=bt, band=frequency, fraction='Third octave')
pt = acoular.TimePower(source=ft)
avgt = acoular.TimeAverage(source=pt, naverage=samples_per_image)

fig = plt.figure(figsize=(10, 7))
cam = Camera(fig)
index: int = 0
for a in avgt.result(1):
    r = a.copy()
    pm = r[0].reshape(rg.shape)
    Lm = acoular.L_p(pm)
    plt.axis("off")
    plt.imshow(Lm.T, vmin=Lm.max() - 15, origin='lower', extent=rg.extend())
    # plt.title('Sekunde %i' % (index + 1))
    # plt.savefig("img/Sekunde" + str(index + 1) + ".png", bbox_inches='tight', pad_inches=0)
    # plt.show()
    print(index + 1, "/", math.floor(ts.numsamples / samples_per_image))
    cam.snap()
    if index == 100:
        break
    index += 1
print("Calculation done... merging to gif")
animation = cam.animate(blit=True, repeat=False, interval=100)
animation.save("img/vid.gif", writer='imagemagick', fps=30)
print("Processing gif")
removeWhitePixels("img/vid.gif")
os.system(
    'ffmpeg -hide_banner -loglevel panic -i {0} -i {1} -filter_complex "[1]format=argb,colorchannelmixer=aa=0.4[front];[front]scale=2230:1216[next];[0][next]overlay=x=-155:y=0,format=yuv420p" {2}'.format(
        "data/4mvid.mp4", "img/vid.gif", "img/overlay.mp4"))
print("Done.")
