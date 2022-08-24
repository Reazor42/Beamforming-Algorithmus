package application;

/*
 * Fortschrittsanzeige für den Enduser sichtbar machen (wie???)
 */


import java.io.File;
import java.io.PrintStream;
import java.io.ByteArrayOutputStream;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.scene.media.MediaView;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.stage.DirectoryChooser;
import javafx.stage.FileChooser;
import javafx.stage.FileChooser.ExtensionFilter;
import javafx.util.Duration;


public class MainWindowController {
	
	/*
	 * declaration of variables and objects that will be needed for beamforming and playing the video
	 */
	private static String configFilePath = null;
	private static String audioPath = null;
	private static String videoPath = null;
	private static String micPath = null;
	private static String distance = null;
	private static String frequency = null;
	
	BeamformingHandler bfh;
	
	Media video;
	MediaPlayer player;
	
	
	
	/**
	 * declare FXML Components
	 */
	@FXML private VBox chooseConfigModeVBox;
	@FXML private VBox manualConfigVBox;
	@FXML private TextField distanceField;
	@FXML private TextField frequencyField;
	@FXML private VBox startBeamformingVBox;
	@FXML private Button goBackButton;
	@FXML private Label progressLabel;
	
	//@FXML private Label progressLabel;
	
	@FXML private MediaView videoView;
	@FXML private Button playVideoButton, pauseVideoButton, resetVideoButton;
	
	
	
	
	/**
	 * Component methods
	 */
	// set the initial visibility
	@FXML private void initialize() {
		manualConfigVBox.setVisible(false);
		chooseConfigModeVBox.setVisible(true);
		startBeamformingVBox.setVisible(false);
		//progressLabel.setVisible(false);
		playVideoButton.setDisable(true);
	}
	
	// let the user choose the config file via a FileChooser
	@FXML private void chooseConfigFile() {
		FileChooser fc = new FileChooser();
		fc.getExtensionFilters().add(new ExtensionFilter("YAML Files", "*.yaml"));
		File f = fc.showOpenDialog(null);
		configFilePath = f.getAbsolutePath();
		chooseConfigModeVBox.setVisible(false); 
		startBeamformingVBox.setVisible(true); 
	}
	
	// show the VBox for manual configuration
	@FXML private void loadManualConfigVBox() {
		chooseConfigModeVBox.setVisible(false);
		manualConfigVBox.setVisible(true);
	}
	
	// DirectoryChooser for the folder with the wav files
	@FXML private void selectAudio() {
		DirectoryChooser dc = new DirectoryChooser();
		File f = dc.showDialog(null);
		audioPath = f.getAbsolutePath();
	}
	
	// FileChooser for the video file
	@FXML private void selectVideo() {
		FileChooser fc = new FileChooser();
		fc.getExtensionFilters().add(new ExtensionFilter("MP4 Files", "*.mp4"));
		File f = fc.showOpenDialog(null);
		videoPath = f.getAbsolutePath();
	}
	
	// FileChooser for the mic32.xml
	@FXML private void selectMicConfig() {
		FileChooser fc = new FileChooser();
		fc.getExtensionFilters().add(new ExtensionFilter("XML Files", "*.xml"));
		File f = fc.showOpenDialog(null);
		micPath = f.getAbsolutePath();
	}
	
	// when the OK button is pressed read out the given paths
	@FXML private void submitManualConfig() {
		distance = distanceField.getText();
		frequency = frequencyField.getText();
		distance = distance.replaceAll(",", "\\.");
		frequency = frequency.replaceAll(",", "\\.");
		
		manualConfigVBox.setVisible(false);
		startBeamformingVBox.setVisible(true);
	}
	
	// go back to the first screen
	@FXML private void loadConfigModeChoice() {
		manualConfigVBox.setVisible(false);
		chooseConfigModeVBox.setVisible(true);
	}
	
	// create a BemformingHandler depending on the users configuration
	// then run the beamforming
	@FXML private void startBeamforming() {
		startBeamformingVBox.setVisible(false);
		System.out.println(startBeamformingVBox.getScene().getWidth());
		startBeamformingVBox.getScene().getWindow().setWidth(startBeamformingVBox.getScene().getWidth() + 0.001);
		System.out.println(startBeamformingVBox.getScene().getWidth());
		
		//if(player != null) removeMedia();
		BeamformingHandler.deleteFiles();
		
		if(configFilePath != null) {
			bfh = new BeamformingHandler(configFilePath);
		}
		else if(distance == null && frequency == null){
			bfh = new BeamformingHandler(audioPath, videoPath, micPath);
		}
		else {
			bfh = new BeamformingHandler(audioPath, videoPath, micPath, distance, frequency);
		}
		
		bfh.runBeamforming();
		
		chooseConfigModeVBox.setVisible(true); 
		addVideo();
	}
	
	// go back to the start screen
	@FXML private void backToStart() {
		startBeamformingVBox.setVisible(false);
		chooseConfigModeVBox.setVisible(true); 
	}
	
	@FXML private void playVideo() {
		player.play();
	}
	
	@FXML private void pauseVideo() {
		player.pause();
	}
	
	@FXML private void resetVideo() {
		if(player.getStatus() != MediaPlayer.Status.READY) {
			player.seek(Duration.seconds(0.0));
		}
	}
	
	
	
	/*
	 * following method is used to add the video created by the beamforming
	 */
	private void addVideo() {
		try {
			video = new Media(new File("overlay.mp4").toURI().toURL().toExternalForm());
			player = new MediaPlayer(video);	
			videoView.setMediaPlayer(player);
			//videoView.fitHeightProperty();
			//videoView.fitWidthProperty();
			videoView.autosize();
			playVideoButton.setDisable(false);
			pauseVideoButton.setDisable(false);
			resetVideoButton.setDisable(false); 
		}
		catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	// this function removes the created video, if there is one
	private void removeMedia() {
		player.dispose();
	}
	
	
	
	/*
	 * this function redirects the console output to a String to show it in the gui
	 */
	public ByteArrayOutputStream redirectOutput() {
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		PrintStream ps = new PrintStream(baos);
		
		//PrintStream oldSysOut = System.out;
		System.setOut(ps);
		return baos;
	}
	
	
	
	/*
	 * instantiate Main
	 */
	public Main main;
	public void setMain(Main main) {
		this.main = main;
	}

}
