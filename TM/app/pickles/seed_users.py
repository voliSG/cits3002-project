import os
import pickle

users = [
    {
        "username": "123",
        "password": "456",
        "questions": [
            {
                "id": "0",
                "language": "python",
                "question": "What is the difference between a list and a tuple?\n a) Lists are immutable, tuples are mutable\n b) Lists are mutable, tuples are immutable\n c) Lists can store any data type while tuples are for integers only \n d) There is no difference\n",
                "type": "mc",
                "attempts": 1,
                "current_answer": "c",
                "correct": False,
            },
            {
                "id": "1",
                "language": "python",
                "question": "Write a program to print the first 10 numbers of the fibonacci sequence\n",
                "type": "code",
                "attempts": 1,
                "current_answer": "print('hello')",
                "correct": False,
            },
            {
                "id": "2",
                "language": "c",
                "question": "What is a pointer?\n a) A pointer is a variable that stores the address of another variable\n b) A pointer is a variable that stores the value of another variable\n c) A pointer is a variable that stores the address of a function\n d) A pointer is a variable that stores the value of a function\n",
                "type": "mc",
                "attempts": 3,
                "current_answer": "a",
                "correct": True,
            },
            {
                "id": "3",
                "language": "python",
                "question": "Write a python program that prints \"Hello world!\"\n",
                "type": "code",
                "attempts": 0,
                "current_answer": "print(\"Hello world!\")",
                "correct": False,
            },
        ],
    },
    {
        "username": "789",
        "password": "101112",
        "questions": [],
    },
    {
        "username": "131415",
        "password": "161718",
        "questions": [],
    },
    {
        "username": "192021",
        "password": "222324",
        "questions": [],
    },
]

full_path = os.path.realpath(__file__)
users_pickle = os.path.join(os.path.dirname(full_path), "users.pickle")

with open(users_pickle, "wb") as pfile:
    pickle.dump(users, pfile)
    print("Users seeded! Yummy!")
    print(users)
