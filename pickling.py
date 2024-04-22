import pickle
import json

# Open the JSON file in read mode.
with open("token.json", "r") as f:
    # Read the contents of the JSON file into a variable.
    json_data = f.read()

# Use the pickle.dumps() function to serialize the JSON object into a byte stream.
pickle_data = pickle.dumps(json_data)

# Open the pickle file in write mode.
with open("token.pickle", "wb") as f:
    # Write the byte stream to the pickle file.
    f.write(pickle_data)

# Close the JSON file and the pickle file.
f.close()
