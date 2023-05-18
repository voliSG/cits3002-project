package exceptions;

public class BadCodeException extends Exception {
    public BadCodeException(String errorMessage) {
        super(errorMessage);
    }
}