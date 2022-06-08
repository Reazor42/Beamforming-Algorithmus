# import the necessary modules
import glob
from scipy.io import wavfile
import numpy as np


# find all wav files in the current working directory
# then sort the list by length
# this puts the files 1-32 in the correct order
wav_list = glob.glob("/home/handschrift/Downloads/gf/220504_03_265Hz_60dB_Links/*.wav")
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
    new_data = data[:minimum_length] # besser: Hälfte vorne und Hälfte hinten abschneiden
    sound_data_list[i] = new_data

# print each element of the list for debug purposes
"""for d in sound_data_list:
    print(len(d), d)"""

# put all data arrays from the sound_data_list together in one 2D-numpy array
# as a result there is an array of shape (32, number_of_samples)
sound_data_array = np.array(sound_data_list[0])
for i in range(1, len(sound_data_list)):
    sound_data_array = np.vstack((sound_data_array, sound_data_list[i]))

# since the array must have the shape (number_of_samples, 32) the array must be transposed
sound_data_array = sound_data_array.T

# print the array and its shape for debug purposes
"""print("\n")
print(sound_data_array)
print("Shape: ", sound_data_array.shape)"""

# create the new wav file that contains the data of all wav files read above
wavfile.write("python/data/data_4/Audio4_265Hz_60dB_Links.wav", 48000, sound_data_array)