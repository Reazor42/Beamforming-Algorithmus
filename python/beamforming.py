import acoular
import matplotlib.pyplot as plt

# Diese Daten hier verändern!
audio_data = "data/test4m.h5"  # name if .h5 audio data
mic_config = "config/mic32.xml"  # path of mic configuration
z_distance = 3  # Kind of the distance to the audio source (kind of)
resolution = 0.1  # the smaller, the sharper
frequency = 550  # band center frequency in hz
samples_per_image = 48000  # 48000 = 1 Second

ts = acoular.TimeSamples(name=audio_data)
mg = acoular.MicGeom(from_file=mic_config)
print(
    f'Bearbeite Audio mit: {ts.numchannels} Channeln; {ts.numsamples} Samples und einer Sample-Frequenz von {ts.sample_freq}Hz')
rg = acoular.RectGrid(x_min=-1, x_max=1,
                      y_min=-1, y_max=1,
                      z=z_distance, increment=resolution)
st = acoular.SteeringVector(grid=rg, mics=mg)

bt = acoular.BeamformerTime(source=ts, steer=st)
ft = acoular.FiltOctave(source=bt, band=frequency, fraction='Third octave')
pt = acoular.TimePower(source=ft)
avgt = acoular.TimeAverage(source=pt, naverage=samples_per_image)

plt.figure(figsize=(10, 7))
i: int = 0
for a in avgt.result(1):
    r = a.copy()
    pm = r[0].reshape(rg.shape)
    Lm = acoular.L_p(pm)
    plt.axis("off")
    plt.imshow(Lm.T, vmin=Lm.max() - 15, origin='lower', extent=rg.extend())
    plt.title('Sekunde %i' % (i + 1))
    plt.savefig("img/Sekunde" + str(i + 1) + ".png")
    plt.show()
    if i == 1500:
        break
    i += 1
