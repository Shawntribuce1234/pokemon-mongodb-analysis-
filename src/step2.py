"""
DS4300 Homework 3 - Step 2
Shawn Tribuce

Reads the locally saved pokemon.json file from Step 1 and imports
all 151 documents into a MongoDB collection using pymongo
"""

import json
import pymongo
INPUT_FILE  = "pokemon.json"        # JSON from Step 1
MONGO_URI   = "mongodb://localhost:27017/"
DB_NAME     = "ds4300_pokemon"      # database name for MongoDB
COLLECTION  = "pokemon"             # collection name

def import_data():
    # Load the JSON file produced in Step 1
    with open(INPUT_FILE, "r") as json_file:
        pokemon_list = json.load(json_file)

    # Connect to MongoDB and get the target collection
    client = pymongo.MongoClient(MONGO_URI)
    db     = client[DB_NAME] # Get the database object (will be created if it doesn't exist)
    col    = db[COLLECTION]  # Get the collection object
    col.drop() # Drop the collection if it already exists

    # Insert all documents in one batch operation
    result = col.insert_many(pokemon_list)

    # Testing if the sample is retrieved correctly
    print("Sample document:")
    sample = col.find_one({}, {"_id": 0})
    print(json.dumps(sample))

    client.close()

if __name__ == "__main__":
    import_data()