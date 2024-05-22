package projekt.IS.DatasetsClient.brokers;

import java.io.File;
import java.io.IOException;

public class PythonBroker {
    public void executePythonScript(String dir, String command) throws IOException {
        ProcessBuilder processBuilder = new ProcessBuilder();
        //String dataDirectory = System.getenv("DATA_DIRECTORY");
        processBuilder.inheritIO();
        processBuilder.directory(new File(dir));
        processBuilder.command(command);
        processBuilder.start();
    }
}
