from scipy.io import wavfile
import tables

# change these variables
wav = ""  # the input wav file
h5 = ""  # the name of the output h5 file

# read data from wav
fs, data = wavfile.read(wav)

folder = ''
# save_to acoular h5 format
acoularh5 = tables.open_file(folder + h5, mode="w", title="test")
acoularh5.create_earray('/', 'time_data', atom=None, title='', filters=None,
                        expectedrows=100000, chunkshape=[256, 64],
                        byteorder=None, createparents=False, obj=data)
acoularh5.set_node_attr('/time_data', 'sample_freq', fs)
acoularh5.close()
