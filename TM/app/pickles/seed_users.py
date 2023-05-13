import os
import pickle

users = [
    {
        "username": "123",
        "password": "456",
        "questions": [
            "What is your favorite color?",
            "What is your favorite food?",
            "What is your favorite animal?",
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
