import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Writer;
import java.util.concurrent.TimeUnit;

public class QBCodeRunner {
    private int timeout = 5;
    private String language = "python";

    public QBCodeRunner() {
    }

    public QBCodeRunner(String language, int timeout) {
        this.language = language;
        this.timeout = timeout;
    }

    public String run(String code) throws IOException, InterruptedException, BadCodeException {
        if (this.language.equals("python")) {
            return runPython(code);
        } else if (this.language.equals("c")) {
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

    private File compileC(File file) throws IOException, InterruptedException {
        Process process = Runtime.getRuntime()
                .exec("cc " + file.getAbsolutePath() + " -o " + file.getAbsolutePath() + ".out");
        process.waitFor(timeout, TimeUnit.SECONDS);

        File outputFile = new File(file.getAbsolutePath() + ".out");

        return outputFile;
    }

    private String runPython(String code) throws IOException, InterruptedException, BadCodeException {
        File file = saveCode(code, ".py");

        // ! the binary is python3 on unix, and python on windows
        Process process = Runtime.getRuntime().exec("python3 " + file.getAbsolutePath());
        process.waitFor(timeout, TimeUnit.SECONDS);

        BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
        BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));

        int exitCode = process.waitFor();

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

        if (exitCode == 0) {
            System.out.println("Python program executed successfully.");
        } else {
            System.out.println("Python program execution failed with exit code: " + exitCode);
            throw new BadCodeException("Code running failed");
        }

        if (error.length() > 0) {
            throw new BadCodeException("runPython code failed");
        }

        return output;
    }

    private String runC(String code) throws IOException, InterruptedException, BadCodeException {
        File file = saveCode(code, ".c");
        File compiledFile = compileC(file);

        Process process = Runtime.getRuntime()
                .exec(compiledFile.getAbsolutePath());
        process.waitFor(timeout, TimeUnit.SECONDS);

        // Read the process output
        BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream(), "UTF-8"));
        BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream(), "UTF-8"));

        // Wait for the process to complete
        int exitCode = process.waitFor();

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

        // Check the exit code
        if (exitCode == 0) {
            System.out.println("C program executed successfully.");
        } else {
            System.out.println("C program execution failed with exit code: " + exitCode);
            throw new BadCodeException("Code running failed");
        }

        if (error.length() > 0) {
            throw new BadCodeException("Code running failed");
        }

        return output;
    }

    public static void main(String[] args) {
        String language = "c";
        int timeout = 5;
        QBCodeRunner runner = new QBCodeRunner(language, timeout);
        try {
            // System.out.println(runner.run("print('Hello World')\nprint('this is a second
            // line')"));
            System.out.println("> " + runner
                    .run("#include <stdio.h>\n\nint main() {\n\tprintf(\"Hello, World!\\n\");\n\treturn 0;\n}"));
        } catch (BadCodeException e) {
            // don't check the answer if the code is bad
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
