import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Writer;
import java.util.concurrent.TimeUnit;

public class QBCodeRunner {
    private int timeout = 5;

    public QBCodeRunner() {
    }

    public QBCodeRunner(int timeout) {
        this.timeout = timeout;
    }

    public String run(String code, String language) throws IOException, InterruptedException {
        if (language.equals("python")) {
            return runPython(code);
        } else if (language.equals("c")) {
            return runC(code);
        } else {
            return "Invalid language";
        }

    }

    private File saveCode(String code, String extension) throws IOException {
        File file = new File("tmp", Integer.toString(code.hashCode()) + extension);
        Writer fileWriter = new FileWriter(file, false);
        fileWriter.write(code);

        fileWriter.flush();
        fileWriter.close();

        return file;
    }

    private void compileC(File file) throws IOException, InterruptedException {
        Process process = Runtime.getRuntime()
                .exec("gcc " + file.getAbsolutePath() + " -o " + file.getAbsolutePath() + ".out");
        process.waitFor(timeout, TimeUnit.SECONDS);
    }

    private String runPython(String code) throws IOException, InterruptedException {
        File file = saveCode(code, ".py");

        // ! the binary is python3 on unix, and python on windows
        Process process = Runtime.getRuntime().exec("python " + file.getAbsolutePath());
        process.waitFor(timeout, TimeUnit.SECONDS);

        BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
        BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));

        String output = "";
        String o = "";
        while ((o = stdInput.readLine()) != null) {
            output += o + "\n";
        }

        String error = "";
        String e = "";
        while ((e = stdError.readLine()) != null) {
            error += e + "\n";
        }

        if (error.length() > 0) {
            return error;
        }

        return output;
    }

    private String runC(String code) throws IOException, InterruptedException {
        File file = saveCode(code, ".c");
        compileC(file);

        return "output";
    }

    public static void main(String[] args) {
        QBCodeRunner runner = new QBCodeRunner();
        try {
            System.out.println(runner.run("print('Hello World')\nprint('this is a second line')", "python"));
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
