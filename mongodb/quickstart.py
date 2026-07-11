import json
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_USERNAME = os.environ["MONGODB_USERNAME"]
MONGODB_PASSWORD = os.environ["MONGODB_PASSWORD"]
MONGODB_HOST = os.environ["MONGODB_HOST"]
MONGODB_APP = os.environ["MONGODB_APP"]

# LOCAL URI
uri = "mongodb://localhost:27017/?directConnection=true"

# CLOUD URI
cloud_uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}/?appName={MONGODB_APP}"

client = MongoClient(cloud_uri)

try:
    database = client.get_database("sample_mflix")
    movies = database.get_collection("movies")

    # Queries for movie that has title 'Back to the future'
    query = {"title": "Back to the Future"}
    movie = movies.find_one(query)

    print(json.dumps(movie, indent=4, default=str))
    client.close()

except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)
