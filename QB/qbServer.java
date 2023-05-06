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

    // Configuration variables
    private static final int NUM_QUESTIONS = 4;
    // Array of QApairs that will be used to store the python questions and answers
    private static QApair[] PythonQuestionBank = {
            new QApair(
                    "What is the difference between a list and a tuple?\n a) Lists are immutable, tuples are mutable\n b) Lists are mutable, tuples are immutable\n c) Lists can store any data type while tuples are for integers only \n d) There is no difference\n",
                    "Lists are mutable, tuples are immutable"),
            new QApair(
                    "What is the order of precedence in python?\n a) Exponential, Parentheses, Multiplication, Division, Addition, Subtraction\n b) Exponential, Parentheses, Division, Multiplication, Addition, Subtraction\n c) Parentheses, Exponential, Multiplication, Division, Subtraction, Addition\n d) Parentheses, Exponential, Multiplication, Division, Addition, Subtraction\n",
                    "d) Parentheses, Exponential, Multiplication, Division, Addition, Subtraction"),
            new QApair(
                    "Write a program to print the first 10 numbers of the fibonacci sequence\n",
                    "a = 0\nb = 1\nfor i in range(10):\n\tprint(a)\n\tc = a + b\n\ta = b\n\tb = c"),
            new QApair("Write a function named lcm to find the LCM of two numbers\n",
                    "def lcm(a, b):\n\tif a > b:\n\t\tgreater = a\n\telse:\n\t\tgreater = b\n\twhile(True):\n\t\tif((greater % a == 0) and (greater % b == 0)):\n\t\t\tlcm = greater\n\t\t\tbreak\n\t\tgreater += 1\n\treturn lcm")
    };

    // Array of QApairs that will be used to store the C questions and answers
    private static QApair[] JavaQuestionBank = new QApair[NUM_QUESTIONS];

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

        // Endpoint for fetching question from the QA pair arrays provided number of
        // questions required in a query parameter called numQuestions, for example
        // /api/question?numQuestions=2
        server.createContext("/api/question", (exchange -> {
            String respText = "";
            int numQuestions = Integer.parseInt(exchange.getRequestURI().getQuery().split("=")[1]);

            // "%k" will separate id from question, while "%e" will separate each
            // id-question pair from each other
            for (int i = 0; i < numQuestions; i++) {
                respText += Integer.toString(i) + " %k " + PythonQuestionBank[i].question + " %e";
            }
            exchange.sendResponseHeaders(200, respText.getBytes().length);
            OutputStream output = exchange.getResponseBody();
            output.write(respText.getBytes());
            output.flush();
            exchange.close();
        }));

        server.setExecutor(null); // creates a default executor
        server.start();

        System.out.println("QB Server running on localhost:" + serverPort + "\n");
    }
}