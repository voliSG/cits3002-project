import os
import pickle

users = [
    {
        "username": "123",
        "password": "456",
        "questions": [],
    },
    {
        "username": "1",
        "password": "1",
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
