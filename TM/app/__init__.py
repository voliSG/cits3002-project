import atexit
import pickle

users_pickle = "app/pickles/users.pickle"

users = []

with open(users_pickle, "rb") as pfile:
    users = pickle.load(pfile)
    print("Users loaded!")
    print(users)


def exit_handler():
    print("Saving users to pickle")
    with open(users_pickle, "wb") as pfile:
        pickle.dump(users, pfile, protocol=pickle.HIGHEST_PROTOCOL)


atexit.register(exit_handler)
