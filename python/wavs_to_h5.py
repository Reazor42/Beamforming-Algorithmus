# import the necessary modules
import glob
from scipy.io import wavfile
import numpy as np
import tables


# =========================================================
# first merge the 32 wav files

# find all wav files in the current working directory
# then sort the list by length
# this puts the files 1-32 in the correct order
wav_list = glob.glob("*.wav")
wav_list.sort(key=len)

# read the wav files and store the sound data (which are numpy arrays) of each file in sound_data_list
sound_data_list = []
for f in wav_list:
    samplerate, data = wavfile.read(f)
    sound_data_list.append(data)

# since the length of the sound data arrays may be slightly different, they must be cut to the same length
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
wavfile.write("merged.wav", 48000, sound_data_array)


# =========================================================
# now create the h5 file

# define the names of the wav file to be read and the h5 file to be written
wav = "merged.wav"
h5 = "sound_data.h5"

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
