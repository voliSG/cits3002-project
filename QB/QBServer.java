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
                    "a)Lists are mutable, tuples are immutable"),
            new QApair(
                    "What is the order of precedence in python?\n a) Exponential, Parentheses, Multiplication, Division, Addition, Subtraction\n b) Exponential, Parentheses, Division, Multiplication, Addition, Subtraction\n c) Parentheses, Exponential, Multiplication, Division, Subtraction, Addition\n d) Parentheses, Exponential, Multiplication, Division, Addition, Subtraction\n",
                    "d) Parentheses, Exponential, Multiplication, Division, Addition, Subtraction"),
            new QApair(
                    "Write a Python program to print the first 10 numbers of the fibonacci sequence\n",
                    "0\n1\n1\n2\n3\n5\n8\n13\n21\n34"),
            new QApair(
                    "Write a python program to print the sum of squares of an array of integers.\nThe initial values of the array are [2, 3, 4] and must be hard coded.",
                    "29")
    };

    // "a = 0\nb = 1\nfor i in range(10):\n\tprint(a)\n\tc = a + b\n\ta = b\n\tb = c"

    // Array of QApairs that will be used to store the C questions and answers
    private static QApair[] CQuestionBank = {
            new QApair(
                    "What is a pointer?\n a) A pointer is a variable that stores the address of another variable\n b) A pointer is a variable that stores the value of another variable\n c) A pointer is a variable that stores the address of a function\n d) A pointer is a variable that stores the value of a function\n",
                    "a) A pointer is a variable that stores the address of another variable"),
            new QApair(
                    "What is memory allocation in C?\n a) Memory allocation is the process of reserving a partial or complete portion of computer memory for the execution of programs and processes\n b) Memory allocation is the process of reserving a partial or complete portion of computer memory for the storage of data\n c) Memory allocation is the process of reserving a partial or complete portion of computer memory for the storage of programs and processes\n d) Memory allocation is the process of reserving a partial or complete portion of computer memory for the execution of data\n",
                    "a) Memory allocation is the process of reserving a partial or complete portion of computer memory for the execution of programs and processes"),
            new QApair(
                    "Write a C program that finds the maximum element in an integer array and prints its value.\nThe initial values of the array are {5, 8, 3, 12, 6}, and must be hard-coded in the program\n",
                    "12"),
            new QApair(
                    "Write a C program that computes the factorial of a given number and prints the result.\nThe initial value of the number is \"5\", must be hard-coded in the program.",
                    "120")
    };




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

        // parsing string to int from argument
        int serverPort = Integer.parseInt(args[0]);
        HttpServer server = HttpServer.create(new InetSocketAddress(serverPort), 0);

        // A variable to store which bank of questions to use based on whether the input
        // is python or c
        QApair[] questionBank = args[1].equals("python") ? PythonQuestionBank : CQuestionBank;

        String logPrefix = "[QBserver - " + args[1] + "] ";

        // Simple endpoint for testing if the server is running and for references
        // purposes. We can remove it later
        server.createContext("/api/hello", (exchange -> {
            String respText = "Hello!\n";
            exchange.sendResponseHeaders(200, respText.getBytes().length);
            OutputStream output = exchange.getResponseBody();
            output.write(respText.getBytes());
            output.flush();
            exchange.close();
        }));

        // Endpoint for fetching questions from the Questions Bank arrays, based on the
        // query parameter, numQuestions, which indicates how many questions should be
        // fetched.
        server.createContext("/api/getQuestions", (exchange -> {
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
            System.out.println(logPrefix + "Sent " + numQuestions + " questions to client!");
        }));

        // Endpoint that returns a boolean based on if the user's response to
        // a question is correct
        // Takes question id and user response parameters
        server.createContext("/api/checkQuestion", (exchange -> {
            System.out.println("checkQuestion");
            String[] params = exchange.getRequestURI().getQuery().split("&");
            // get question id
            int qid = Integer.parseInt(params[0].split("=")[1]);

            // get user answer
            String user_answer = params[1].split("=")[1];

            // init responseBool which holds if question is correct or incorrect
            String respText = "False";

            // retreive expected answer (mcq)
            String expected_answer = questionBank[qid].answer;

            if (user_answer.equals(expected_answer)) {
                respText = "True";
            }

            exchange.sendResponseHeaders(200, respText.getBytes().length);
            OutputStream output = exchange.getResponseBody();
            output.write(respText.getBytes());
            output.flush();
            exchange.close();
            System.out.println("Response Correct?: " + respText);
        }));


        server.setExecutor(null); // creates a default executor
        server.start();

        System.out.println("QB Server running on localhost:" + serverPort + "\n");
    }
}