// Reference used to implement QB: 
// Setting up a REST API in pure Java: https://medium.com/consulner/framework-less-rest-api-in-java-dd22d4d642fa

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.Buffer;

import com.sun.net.httpserver.HttpServer;

import banks.CBank;
import banks.PythonBank;
import banks.QAPair;
import enums.Language;
import enums.QuestionType;
import exceptions.BadCodeException;

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
        server.createContext("/api/hello", (exchange -> {
            String respText = "Hello!\n";
            exchange.sendResponseHeaders(200, respText.getBytes().length);
            OutputStream output = exchange.getResponseBody();
            output.write(respText.getBytes());
            output.flush();
            exchange.close();
        }));

        // Simple endpoint for testing if the server is running and for references
        // purposes. We can remove it later

        // Endpoint for fetching questions from the Questions Bank arrays, based on the
        // query parameter, numQuestions, which indicates how many questions should be
        // fetched.
        server.createContext("/api/questions", (exchange -> {
            String respText = "";
            int numQuestions = Integer.parseInt(exchange.getRequestURI().getQuery().split("=")[1]);

            // "%k" will separate id from question, while "%e" will separate each
            // id-question pair from each other

            // storing a numQuestion random numbers between 1 to numQuestions into an int
            // array
            // this is done to ensure that the questions are chosen randomly and not
            // repeated
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
                respText += Integer.toString(i) + " %k " + questionBank[randomNumbers[i]].question + " %e";
            }
            exchange.sendResponseHeaders(200, respText.getBytes().length);
            OutputStream output = exchange.getResponseBody();
            output.write(respText.getBytes());
            output.flush();
            exchange.close();
            System.out.println(
                    "[QBserver - " + language.toString() + "]" + "Sent " + numQuestions + " questions to client!");
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
            // ! this isn't working for some reason
            int qId = Integer.parseInt(params[0].split("=")[1]);

            // get user answer (second param)
            String answer = params[1].split("=")[1];

            // init responseBool which holds if question is correct or incorrect
            String response = "false";

            System.out.println("Question ID: " + qId);

            QAPair question = questionBank[qId];

            // if question requires code input, run code and save output as user_answer
            if (question.type == QuestionType.CODE) {
                System.out.println("Code question");
                try {
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