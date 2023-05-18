package banks;

import enums.QuestionType;

public class QAPair {
    public QuestionType type;
    public String question;
    public String answer;
    public String sampleAnswer;

    public QAPair(QuestionType type, String question, String answer, String sampleAnswer) {
        this.type = type;
        this.question = question;
        this.answer = answer;
        this.sampleAnswer = sampleAnswer;
    }

}
