package application;


import java.io.File;
import java.net.MalformedURLException;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.scene.media.MediaView;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;


public class MainWindowController {
	
	/*
	 * declaration of variables and objects that will be needed for beamforming and playing the video
	 */
	private static String configFilePath;
	private static String audioPath;
	private static String videoPath;
	private static String micPath;
	
	BeamformingHandler bfh;
	
	Media video;
	MediaPlayer player;
	
	
	
	/**
	 * declare FXML Components
	 */
	@FXML private VBox chooseConfigModeVBox;
	@FXML private ChoiceBox<String> configModeChoiceBox;
	@FXML private Button submitConfigModeButton;
	
	@FXML private VBox autoConfigVBox;
	@FXML private TextField configFilePathField;
	@FXML private Button submitConfigFilePathButton;
	@FXML private Button backToModeChoiceButton;
	
	@FXML private VBox manualConfigVBox;
	@FXML private TextField audioPathField;
	@FXML private TextField videoPathField;
	@FXML private TextField micPathField;
	
	@FXML private Button startBeamformingButton;
	
	@FXML private MediaView videoView;
	@FXML private Button playVideoButton;
	
	
	// create a list with options for the choice box
	private final String optionAuto = "automatisch (über Konfigurationsdatei)";
	private final String optionManual = "manuell";
	ObservableList<String> configModeList = FXCollections.observableArrayList(optionAuto, optionManual);
	
	
	
	/**
	 * Component methods
	 */
	@FXML private void initialize() {
		autoConfigVBox.setVisible(false); 
		manualConfigVBox.setVisible(false); 
		chooseConfigModeVBox.setVisible(true);
		startBeamformingButton.setVisible(false);
		playVideoButton.setDisable(true); 
		configModeChoiceBox.setItems(configModeList);
	}
	
	@FXML private void enableSubmitChoiceButton() {
		submitConfigModeButton.setDisable(false);
	}
	
	@FXML private void loadConfigMode() {
		String configMode = configModeChoiceBox.getValue();
		chooseConfigModeVBox.setVisible(false);
		if(configMode == optionAuto) {
			autoConfigVBox.setVisible(true);
		}
		else {
			manualConfigVBox.setVisible(true); 
		}
	}
	
	@FXML private void submitConfigFilePath() {
		configFilePath = configFilePathField.getText();
		autoConfigVBox.setVisible(false);
		startBeamformingButton.setVisible(true); 
	}
	
	@FXML private void loadConfigModeChoice() {
		autoConfigVBox.setVisible(false);
		manualConfigVBox.setVisible(false); 
		chooseConfigModeVBox.setVisible(true);
	}
	
	@FXML private void submitManualPaths() {
		audioPath = audioPathField.getText();
		videoPath = videoPathField.getText();
		micPath = micPathField.getText();
		manualConfigVBox.setVisible(false);
		startBeamformingButton.setVisible(true); 
	}
	
	@FXML private void startBeamforming() {
		startBeamformingButton.setVisible(false);
		
		if(configFilePath != null) {
			bfh = new BeamformingHandler(configFilePath);
		}
		else {
			bfh = new BeamformingHandler(audioPath, videoPath, micPath);
		}
		bfh.runBeamforming();
		addVideo();
	}
	
	@FXML private void playVideo() {
		//player.
		player.play();
	}
	
	
	
	/*
	 * following method is used to add the video created by the beamforming
	 */
	private void addVideo() {
		try{
			video = new Media(new File("overlay.mp4").toURI().toURL().toExternalForm());
			player = new MediaPlayer(video);
			videoView.setMediaPlayer(player);
			videoView.fitHeightProperty();
			videoView.fitWidthProperty();
			playVideoButton.setDisable(false); 
		}
		catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	
	
	/*
	 * instantiate Main
	 */
	public Main main;
	public void setMain(Main main) {
		this.main = main;
	}

}
