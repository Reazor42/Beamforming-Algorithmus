package application;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;

public class MainWindowController {
	
	/**
	 * Views
	 */
	@FXML private Label pathLabel;
	@FXML private TextField pathField;
	
	public Main main;
	
	public void setMain(Main main) {
		this.main = main;
	}
	
	
	@FXML
	public void submit() {
		String text = pathField.getText();
		pathLabel.setText(text);
	}
	
	@FXML
	public void cancel() {
		pathLabel.setText("Text eingeben:");
		pathField.clear();
	}

}
