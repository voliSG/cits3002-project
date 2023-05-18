package banks;

public final class PythonBank {
    public static final QAPair[] questions = {
            new QAPair(
                    "What is the difference between a list and a tuple?\n a) Lists are immutable, tuples are mutable\n b) Lists are mutable, tuples are immutable\n c) Lists can store any data type while tuples are for integers only \n d) There is no difference\n",
                    "a", "Lists are immutable, tuples are mutable"),
            new QAPair(
                    "What is the order of precedence in python?\n a) Exponential, Parentheses, Multiplication, Division, Addition, Subtraction\n b) Exponential, Parentheses, Division, Multiplication, Addition, Subtraction\n c) Parentheses, Exponential, Multiplication, Division, Subtraction, Addition\n d) Parentheses, Exponential, Multiplication, Division, Addition, Subtraction\n",
                    "d", "Parentheses, Exponential, Multiplication, Division, Addition, Subtraction"),
            new QAPair(
                    "Write a Python program to print the first 10 numbers of the fibonacci sequence\n",
                    "0\n1\n1\n2\n3\n5\n8\n13\n21\n34\n",
                    "def fibonacci(n):\nif n == 0:\nreturn 0\nelif n == 1:\nreturn 1\nelse:\nreturn fibonacci(n - 1) + fibonacci(n - 2)"),
            new QAPair(
                    "Write a python program to print the sum of squares of an array of integers.\nThe initial values of the array are [2, 3, 4] and must be hard coded.",
                    "29\n",
                    "def sum_of_squares(arr):\nsum = 0\nfor i in arr:\nsum += i ** 2\nreturn sum\n\nprint(sum_of_squares([2, 3, 4]))\n# Output: 29\n")
    };
}