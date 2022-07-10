package application;
	
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;


public class Main extends Application {
	
	private Stage primaryStage;
	
	@Override
	public void start(Stage primaryStage) {
		this.primaryStage = primaryStage;
		mainWindow();
	}
	
	public void mainWindow() {
		try {
			FXMLLoader loader = new FXMLLoader(Main.class.getResource("MainWindow.fxml"));
			AnchorPane pane = loader.load();
			
			primaryStage.setMinWidth(1100);
			primaryStage.setMinHeight(650);
			
			MainWindowController mwc = loader.getController();
			mwc.setMain(this);
			
			Scene scene = new Scene(pane);
			primaryStage.setScene(scene);
			primaryStage.show();
			
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		launch(args);
	}
}

