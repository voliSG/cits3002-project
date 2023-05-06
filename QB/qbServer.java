// Reference used to implement QB: 
// Setting up a REST API in pure Java: https://medium.com/consulner/framework-less-rest-api-in-java-dd22d4d642fa
//

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.HttpServer;

class QBserver {
    // an object called QApair that stores two string values, a question and an
    // answer
    static class QApair {
        String question;
        String answer;

        public QApair(String question, String answer) {
            this.question = question;
            this.answer = answer;
        }
    }

    private final int NUM_QUESTIONS = 4;

    // Array of QApairs that will be used to store the python questions and answers
    private QApair[] PythonQuestionBank = new QApair[NUM_QUESTIONS];

    // Array of QApairs that will be used to store the C questions and answers
    private QApair[] JavaQuestionBank = new QApair[NUM_QUESTIONS];

    public static void main(String[] args) throws IOException {
        if (args.length != 2) {
            System.out.println("Usage: java QBserver <port> <language [python/c]>");
            System.exit(1);
        }

        // parsing string to int from argument
        int serverPort = Integer.parseInt(args[0]);
        HttpServer server = HttpServer.create(new InetSocketAddress(serverPort), 0);

        server.createContext("/api/hello", (exchange -> {
            String respText = "Hello!\n";
            exchange.sendResponseHeaders(200, respText.getBytes().length);
            OutputStream output = exchange.getResponseBody();
            output.write(respText.getBytes());
            output.flush();
            exchange.close();
        }));

        // Endpoint for fetching

        server.setExecutor(null); // creates a default executor
        server.start();

        System.out.println("QB Server running on localhost:" + serverPort + "\n");
    }
}