import os
import pickle

users = [
    {
        "username": "123",
        "password": "456",
        "questions": [],
        "score": 0,
    },
    {
        "username": "1",
        "password": "1",
        "questions": [],
        "score": 0,
    },
    {
        "username": "131415",
        "password": "161718",
        "questions": [],
        "score": 0,
    },
    {
        "username": "192021",
        "password": "222324",
        "questions": [],
        "score": 0,
    },
]

full_path = os.path.realpath(__file__)
users_pickle = os.path.join(os.path.dirname(full_path), "users.pickle")

with open(users_pickle, "wb") as pfile:
    pickle.dump(users, pfile)
    print("Users seeded! Yummy!")
    print(users)
