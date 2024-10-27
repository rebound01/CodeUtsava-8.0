import requests
import json
from pymongo import MongoClient

# Pinata API credentials
PINATA_API_KEY = "b13660699821ca0dbfb5"
PINATA_SECRET_API_KEY = "444a74c9a44e579077122e3ca01a49f020a6ff6a9e5248f512d8d05115dcab94"

# MongoDB configuration
MONGO_URI = "mongodb+srv://hackathon:yaHAVKDwVLgNEFVN@cluster0.eer9i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB URI if different
DATABASE_NAME = "face_recognition"  # Replace with your actual database name
COLLECTION_NAME = "face_embeddings"    # Replace with your actual collection name

# Function to upload data to IPFS
def upload_to_ipfs(data):
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["IpfsHash"]
    else:
        raise Exception("Error uploading to IPFS: " + response.text)

# Function to fetch data from MongoDB
def fetch_data_from_mongodb():
    # Create a MongoDB client
    client = MongoClient(MONGO_URI)

    # Access the database and collection
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Retrieve all documents from the collection
    documents = list(collection.find())

    # Convert ObjectId to string and return the documents
    for document in documents:
        document['_id'] = str(document['_id'])  # Convert ObjectId to string
    
    # Close the client connection
    client.close()
    
    return documents

# Fetch data from MongoDB
data_from_mongodb = fetch_data_from_mongodb()

# Upload the data to IPFS
for data in data_from_mongodb:
    ipfs_hash = upload_to_ipfs(data)
    print("Uploaded data:", data)
    print("IPFS Hash:", ipfs_hash)