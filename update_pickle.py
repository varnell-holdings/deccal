import pickle

# Saving data
my_string = (1, 1, 2025)
with open("saved_data.pkl", "wb") as file:
    pickle.dump(my_string, file)

# Loading data in a later run
# with open("saved_data.pkl", "rb") as file:
#     loaded_string = pickle.load(file)
# print(loaded_string)
