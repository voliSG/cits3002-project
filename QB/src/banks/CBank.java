package banks;

import enums.QuestionType;

public class CBank {
        public static final QAPair[] questions = {
                        new QAPair(
                                        QuestionType.MC,
                                        "What is a pointer?\n a) A pointer is a variable that stores the address of another variable\n b) A pointer is a variable that stores the value of another variable\n c) A pointer is a variable that stores the address of a function\n d) A pointer is a variable that stores the value of a function\n",
                                        "a",
                                        "A pointer is a variable that stores the address of another variable"),
                        new QAPair(
                                        QuestionType.MC,

                                        "What is memory allocation in C?\n a) Memory allocation is the process of reserving a partial or complete portion of computer memory for the execution of programs and processes\n b) Memory allocation is the process of reserving a partial or complete portion of computer memory for the storage of data\n c) Memory allocation is the process of reserving a partial or complete portion of computer memory for the storage of programs and processes\n d) Memory allocation is the process of reserving a partial or complete portion of computer memory for the execution of data\n",
                                        "a",
                                        "Memory allocation is the process of reserving a partial or complete portion of computer memory for the execution of programs and processes"),
                        new QAPair(
                                        QuestionType.CODE,
                                        "Write a C program that finds the maximum element in an integer array and prints its value.\nThe initial values of the array are {5, 8, 3, 12, 6}, and must be hard-coded in the program\n",
                                        "12\n",
                                        // "int main()\n{\n\tint arr[] = {5, 8, 3, 12, 6};\n\tint max = arr[0];\n\tfor
                                        // (int i = 1; i < 5; i++)\n\t{\n\t\tif (arr[i] > max)\n\t\t{\n\t\t\tmax =
                                        // arr[i];\n\t\t}\n\t}\n\tprintf('%d\\n', max);\n\treturn 0;\n}",
                                        "/images/c_q3.png"),
                        new QAPair(
                                        QuestionType.CODE,
                                        "Write a C program that computes the factorial of a given number and prints the result.\nThe initial value of the number is '5', must be hard-coded in the program.",
                                        "120\n",
                                        // "int main()\n{\n\tint n = 5;\n\tint factorial = 1;\n\tfor (int i = 1; i <= n;
                                        // i++)\n\t{\n\t\tfactorial *= i;\n\t}\n\tprintf('%d\\n', factorial);\n\treturn
                                        // 0;\n}",
                                        "/images/c_q4.png")
        };
}
