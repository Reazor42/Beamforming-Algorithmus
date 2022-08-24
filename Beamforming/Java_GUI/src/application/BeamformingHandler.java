package application;


import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;


public class BeamformingHandler {
	
	/*
	 * declaration of variables for needed paths
	 */
	private String configFilePath;
	private String audioPath;
	private String videoPath;
	private String micPath;
	private String distance;
	private String frequency;
	
	public boolean beamformingCompleted = false;
	
	public Process p;
	
	/*
	 * define some constructors for different use cases
	 */
	public BeamformingHandler(String configFilePath) {
		this.configFilePath = configFilePath;
	}
	
	public BeamformingHandler(String audioPath, String videoPath, String micPath) {
		this.audioPath = audioPath;
		this.videoPath = videoPath;
		this.micPath = micPath;
	}

	public BeamformingHandler(String audioPath, String videoPath, String micPath, String distance, String frequency) {
		this.audioPath = audioPath;
		this.videoPath = videoPath;
		this.micPath = micPath;
		this.distance = distance;
		this.frequency = frequency;
	}
	
	
	
	/*
	 * start the beamforming by running the python script
	 */
	public void runBeamforming() {
		
		try {
			String pythonScriptPath = "C:/Users/marc.andresen/Documents/GitHub/Beamforming-Algorithmus/Beamforming/Python_Beamforming/main.py";
			
			ProcessBuilder pb;			
			if(configFilePath != null) {
				pb = new ProcessBuilder("python", pythonScriptPath, "--file", configFilePath).inheritIO();
			}
			else if(distance == null & frequency == null) {
				pb = new ProcessBuilder("python" , pythonScriptPath, "--audio", audioPath, "--video", videoPath, "--array", micPath).inheritIO();
			}
			else if(distance != null & frequency == null) {
				pb = new ProcessBuilder("python" , pythonScriptPath, "--audio", audioPath, "--video", videoPath, "--array", micPath, "--distance", distance).inheritIO();
			}
			else if(distance == null & frequency != null) {
				pb = new ProcessBuilder("python" , pythonScriptPath, "--audio", audioPath, "--video", videoPath, "--array", micPath, "--frequency", frequency).inheritIO();
			}
			else {
				pb = new ProcessBuilder("python" , pythonScriptPath, "--audio", audioPath, "--video", videoPath, "--array", micPath, "--distance", distance, "--frequency", frequency).inheritIO();
			}
			
			p = pb.start();
			p.waitFor();
		}
		catch(Exception e) {
			e.printStackTrace();
		}
		
//		try {
//			Thread.sleep(5000);
//		}
//		catch(Exception e) {}
		
	}
	
	
	
	/*
	 * this function deletes the h5 file and the mp4 file if necessary
	 */
	public static void deleteFiles() {
		String mp4File = "./overlay.mp4";
		String h5File = "./sound_data.h5";
		
		Path mp4Path = Paths.get(mp4File);
		Path h5Path = Paths.get(h5File);
		try {
			Files.deleteIfExists(mp4Path);
			Files.deleteIfExists(h5Path);
		}
		catch(Exception e) {
			e.printStackTrace();
		}
	}
	
}
