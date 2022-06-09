import functions

path = r"C:\Users\marc.andresen\Desktop\Tonaufnahmen\220504_03_442Hz_60dB_Links"
video_name = r"WIN_20220504_16_57_16_Pro.mp4"

print("merging waves")
merged_wav = functions.merge_waves(path)
print("converting to h5")
h5 = functions.wav2h5(merged_wav)
print("starting beamforming")
functions.beamforming(h5, path + "\\" + video_name)


