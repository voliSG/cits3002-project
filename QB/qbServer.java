// Reference used to implement QB: 
// Setting up a REST API in pure Java: https://medium.com/consulner/framework-less-rest-api-in-java-dd22d4d642fa
//

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.HttpServer;

class QBserver {
    public static void main(String[] args) throws IOException {

        int serverPort = 8001;
        HttpServer server = HttpServer.create(new InetSocketAddress(serverPort), 0);
        server.createContext("/api/hello", (exchange -> {
            String respText = "Hello!\n";

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