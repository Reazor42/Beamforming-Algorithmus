import functions
from Config import Config

if __name__ == '__main__':
    args = functions.parse_arguments()
    config = Config()
    if args.file is None:
        # Throw an exception if one of the required parameters is not provided
        if args.audio or args.video or args.array is None:
            raise Exception(
                "You have to provide at least the audio path the video path and the array config path or a config "
                "file as command line parameters!")
        config.init_values(args.audio, args.video, args.fps, args.frequency, args.distance, args.array, args.resolution,
                           args.x_min,
                           args.x_max, args.y_min, args.y_max, args.output, args.transparency, args.min_volume)
    else:
        config.parse_from_yaml(args.file)

    path = config.audio
    video_name = config.video

    print("merging waves")
    merged_wav = functions.merge_waves(path)
    print("converting to h5")
    h5 = functions.wav2h5(merged_wav)
    print("starting beamforming")
    functions.beamforming(h5, config)
