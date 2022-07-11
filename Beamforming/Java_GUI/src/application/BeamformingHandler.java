package application;


public class BeamformingHandler {
	
	/*
	 * declaration of variables for needed paths
	 */
	private String configFilePath;
	private String audioPath;
	private String videoPath;
	private String micPath;
	
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
	
	
	
	/*
	 * start the beamforming by running the python script
	 */
	public void runBeamforming() {
		
		try {
			String pythonExePath = "Python_Interpreter/python.exe";
			String pythonScriptPath = "C:/Users/marc.andresen/Documents/GitHub/Beamforming-Algorithmus/Beamforming/Python_Beamforming/main.py";
			
			ProcessBuilder pb;			
			if(configFilePath != null) {
				pb = new ProcessBuilder(pythonExePath, pythonScriptPath, "--file", configFilePath).inheritIO();
			}
			else {
				pb = new ProcessBuilder(pythonExePath, pythonScriptPath, "--audio", audioPath, "--video", videoPath, "--array", micPath).inheritIO();
			}
			
			Process p = pb.start();
			p.waitFor();
		}
		catch(Exception e) {
			e.printStackTrace();
		}
		
	}
	
}
