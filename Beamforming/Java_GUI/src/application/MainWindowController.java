package application;


import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;


public class MainWindowController {
	
	/**
	 * declare Components
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
		String path = configFilePathField.getText();
		autoConfigVBox.setVisible(false);
	}
	
	@FXML private void loadConfigModeChoice() {
		autoConfigVBox.setVisible(false);
		manualConfigVBox.setVisible(false); 
		chooseConfigModeVBox.setVisible(true);
	}
	
	@FXML private void submitManualPaths() {
		String audioPath = audioPathField.getText();
		String videoPath = videoPathField.getText();
		String micPath = micPathField.getText();
		//manualConfigVBox.setVisible(false);
	}
	
	
	
	/*
	 * instantiate Main
	 */
	public Main main;
	public void setMain(Main main) {
		this.main = main;
	}

}
