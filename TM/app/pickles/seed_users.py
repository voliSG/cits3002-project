import os
import pickle

users = [
    {"username": "123", "password": "456"},
    {"username": "789", "password": "101112"},
    {"username": "131415", "password": "161718"},
    {"username": "192021", "password": "222324"},
]

full_path = os.path.realpath(__file__)
users_pickle = os.path.join(os.path.dirname(full_path), "users.pickle")

with open(users_pickle, "wb") as pfile:
    pickle.dump(users, pfile)
    print("Users seeded! Yummy!")
