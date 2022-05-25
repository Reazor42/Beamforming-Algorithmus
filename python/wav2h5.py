from scipy.io import wavfile
import tables
import h5py

# change these variables
wav = "data/data_11/out_multi.wav"  # the input wav file
h5 = "data/data_11/out_multi.h5"  # the name of the output h5 file

# read data from wav
fs, data = wavfile.read(wav)

folder = ''
# save_to acoular h5 format
with h5py.File(h5, 'w') as data_file:
    data_file.create_dataset('time_data', data=data)
    data_file['time_data'].attrs.__setitem__('sample_freq', 48000)

"""with h5py.File(h5, 'w') as data_file:
    data_file.create_dataset('time_data', data=data)
    data_file['time_data'].attrs.__setitem__('sample_freq', fs)"""
