import pickle

users_pickle = "app/pickles/users.pickle"

users = []

with open(users_pickle, "rb") as pfile:
    users = pickle.load(pfile)
