// Setting up a REST API in pure Java: https://medium.com/consulner/framework-less-rest-api-in-java-dd22d4d642fa

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.File;
import java.nio.file.Files;
import java.net.InetSocketAddress;
import java.net.URLDecoder;

import com.sun.net.httpserver.HttpServer;

import banks.CBank;
import banks.PythonBank;
import banks.QAPair;
import enums.Language;
import enums.QuestionType;
import exceptions.BadCodeException;
import util.QBCodeRunner;

public class QBServer {
    private static final int NUM_QUESTIONS = 4;

    private HttpServer server;
    private int serverPort;
    private Language language;
    private QBCodeRunner runner;

    QAPair[] questionBank;

    public QBServer(Language language, int serverPort) throws IOException {
        this.language = language;
        this.serverPort = serverPort;

        questionBank = language == Language.PYTHON ? PythonBank.questions : CBank.questions;
    }

    public void start() throws IOException {
        server = HttpServer.create(new InetSocketAddress(serverPort), 0);
        runner = new QBCodeRunner(language, 5);
        loadEndpoints();

        server.setExecutor(null); // creates a default executor
        server.start();
    }

    private void loadEndpoints() {
        // Simple endpoint for testing response
        server.createContext("/api/hello", (exchange -> {

            // manually creating a json string
            String respText = "{\n\t\"message\": \"Hello!\"\n}";

            exchange.getResponseHeaders().set("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, respText.getBytes().length);
            OutputStream output = exchange.getResponseBody();
            output.write(respText.getBytes());
            output.flush();
            exchange.close();
        }));

        // Endpoint for fetching questions from question banks based on the parameter
        // numQuestions, which indicates how many questions should be fetched.
        server.createContext("/api/getQuestions", (exchange -> {
            String respText = "{\n\t\"questions\": [\n";
            int numQuestions = Integer.parseInt(exchange.getRequestURI().getQuery().split("=")[1]);
            int[] randomNumbers = new int[numQuestions];
            for (int i = 0; i < numQuestions; i++) {
                randomNumbers[i] = (int) (Math.random() * questionBank.length);
                for (int j = 0; j < i; j++) {
                    if (randomNumbers[i] == randomNumbers[j]) {
                        i--;
                        break;
                    }
                }
            }

            for (int i = 0; i < numQuestions; i++) {
                QAPair question = questionBank[randomNumbers[i]];
                respText += "\t\t{\n\t\t\t\"id\": " + randomNumbers[i] + ",\n\t\t\t\"question\": \""
                        + question.question.replace("\n", "\\n") + "\",\n\t\t\t\"type\": \""
                        + question.type + "\"\n\t\t}";
                if (i != numQuestions - 1) {
                    respText += ",\n";
                } else {
                    respText += "\n\t]";
                }
            }

            respText += "\n}";

            exchange.sendResponseHeaders(200, respText.getBytes().length);
            OutputStream output = exchange.getResponseBody();
            output.write(respText.getBytes());
            output.flush();
            exchange.close();
            System.out.println(
                    "[QBserver - " + language.toString() + "]" + "Sent " + numQuestions + " questions to client!");
        }));

        // Endpoint that fetches the sample response for mcq and code questions
        // Takes question id as parameters
        server.createContext("/api/questions/sample", (exchange -> {
            // get question id
            int qId = Integer.parseInt(exchange.getRequestURI().getQuery().split("=")[1]);

            QAPair question = questionBank[qId];
            String sampleAnswer = question.sampleAnswer;

            exchange.sendResponseHeaders(200, sampleAnswer.getBytes().length);
            OutputStream output = exchange.getResponseBody();
            output.write(sampleAnswer.getBytes());
            output.flush();
            exchange.close();
        }));

        // Endpoint that returns a boolean based on if the user's response to
        // a question is correct
        // Takes question id and user response parameters
        server.createContext("/api/questions/check", (exchange -> {
            // String query = exchange.getRequestURI().getQuery();
            // System.out.println("Hello" + query);
            // String[] params = query.split("&");
            System.out.println("Checking question");

            InputStreamReader isr = new InputStreamReader(exchange.getRequestBody(), "utf-8");
            BufferedReader br = new BufferedReader(isr);

            int b;
            StringBuilder buf = new StringBuilder();
            while ((b = br.read()) != -1) {
                buf.append((char) b);
            }

            br.close();
            isr.close();

            String body = buf.toString();

            System.out.println(body);

            String[] params = body.split("&");

            // get question id (first param)
            int qId = Integer.parseInt(params[0].split("=")[1]);

            // get user answer (second param)
            String answer = URLDecoder.decode(params[1].split("=")[1], "UTF-8");

            // init responseBool which holds if question is correct or incorrect
            String response = "false";

            System.out.println("Question ID: " + qId);

            QAPair question = questionBank[qId];

            // if question requires code input, run code and save output as user_answer
            if (question.type == QuestionType.CODE) {
                System.out.println("Code question");
                try {
                    System.out.println(answer);
                    answer = runner.run(answer);
                } catch (BadCodeException e) {
                    // terminate early if code is bad
                    response = "false";
                    exchange.sendResponseHeaders(200, response.getBytes().length);
                    exchange.sendResponseHeaders(200, response.getBytes().length);
                    OutputStream output = exchange.getResponseBody();
                    output.write(response.getBytes());
                    output.flush();
                    exchange.close();
                    return;
                } catch (IOException | InterruptedException e) {
                    e.printStackTrace();
                }
            }

            // retreive expected answer (mcq)
            String expectedAnswer = question.answer;

            if (answer.equals(expectedAnswer)) {
                response = "true";
            }

            exchange.sendResponseHeaders(200, response.getBytes().length);
            OutputStream output = exchange.getResponseBody();
            output.write(response.getBytes());
            output.flush();
            exchange.close();
            System.out.println("Response Correct?: " + response);
        }));

        // an endpoint to serve image files
        server.createContext("/images", (exchange -> {
            String path = exchange.getRequestURI().getPath();
            String fileName = path.substring(path.lastIndexOf("/") + 1);
            File file = new File("images/" + fileName);
            exchange.sendResponseHeaders(200, file.length());
            OutputStream output = exchange.getResponseBody();
            Files.copy(file.toPath(), output);
            output.flush();
            exchange.close();
        }));
    }

    public static void main(String[] args) throws IOException {
        if (args.length != 2) {
            System.out.println("Usage: java QBserver <port> <language [python/c]>");
            System.exit(1);
        } else {
            if (!args[1].equals("python") && !args[1].equals("c")) {
                System.out.println("Usage: java QBserver <port> <language [python/c]>");
                System.out.println("Language must be either python or c");
                System.exit(1);
            }
        }

        int serverPort = Integer.parseInt(args[0]);
        Language language = args[1].equals("c") ? Language.C : Language.PYTHON;

        QBServer server = new QBServer(language, serverPort);

        server.start();

        System.out.println("QB Server running on localhost:" + serverPort + "\n");
    }
}