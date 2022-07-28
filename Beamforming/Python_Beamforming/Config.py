import yaml


class Config:
    """
    A class representing the config file for the beamforming.

    Attributes
    ----------
    audio:
        path to the dictionary containing the wav files
    video:
        path to the video file
    array:
        path to the array configuration (xml) file
    fps:
        frames per second for the beamforming overlay
    frequency:
        band center frequency for the beamforming
    distance:
        distance between the microphone array and the sound source
    resolution:
        resolution of the acoustic map
    output:
        path where the resulting video and the temporary files should be saved
    x_min, y_min, x_max, y_max
        dimensions of the acoustic pane
    """

    def __init__(self):
        self.audio: str = ""
        self.video: str = ""
        self.array: str = ""
        self.fps: int = 10
        self.frequency: int = 550
        self.distance: int = 3
        self.resolution: float = 0.5
        self.x_min: float = - 3.0
        self.x_max: float = 3.0
        self.y_min: float = -2.1
        self.y_max: float = 2.1
        self.output: str = "."

    def init_values(self, audio: str, video: str, fps: int, frequency: int, distance: int
                    , array: str, resolution: float, x_min: float, x_max: float, y_min: float, y_max: float,
                    output: str) -> None:
        """
        Initializing attributes of the config by directly providing them
        :param audio:
        :param video:
        :param fps:
        :param frequency:
        :param distance:
        :param array:
        :param resolution:
        :param x_min:
        :param x_max:
        :param y_min:
        :param y_max:
        :param output: 
        """
        self.audio: str = audio
        self.video: str = video
        self.fps: int = fps
        self.frequency: int = frequency
        self.distance: int = distance
        self.resolution: float = resolution
        self.x_min: float = x_min
        self.x_max: float = x_max
        self.y_min: float = y_min
        self.y_max: float = y_max
        self.array: str = array
        self.output: str = output

    def parse_from_yaml(self, path: str) -> None:
        """
        Initializes attributes of the config by parsing a yaml file.

        :param path: path to the yaml file
        """
        with open(path, 'r') as yaml_file:
            data: dict = yaml.safe_load(yaml_file)
            self.audio: str = data["audio"]
            self.video: str = data["video"]
            self.fps: int = data["fps"]
            self.frequency: int = data["frequency"]
            self.distance: int = data["distance"]
            self.resolution: float = data["resolution"]
            self.x_min: float = data["x_min"]
            self.x_max: float = data["x_max"]
            self.y_min: float = data["y_min"]
            self.y_max: float = data["y_max"]
            self.array: str = data["array"]
            self.output: str = data["output"]
