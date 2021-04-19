import pymongo
import pandas as pd
import boto3

from boto.s3.connection import S3Connection
from sys import argv, exit

# Prepare the SSM client
ssm = boto3.client('ssm')

# Secrets
MONGO_HOST=ssm.get_parameter(Name="/prod/mongodb/host", WithDecryption=True)['Parameter']['Value']
MONGO_USER=ssm.get_parameter(Name="/prod/mongodb/username", WithDecryption=True)['Parameter']['Value']
MONGO_PASSWORD=ssm.get_parameter(Name="/prod/mongodb/password", WithDecryption=True)['Parameter']['Value']
MONGO_AUTH_SOURCE=ssm.get_parameter(Name="/prod/mongodb/auth_source", WithDecryption=True)['Parameter']['Value']

# Chunk size to read the
CHUNK_SIZE=10000

DOCUMENT_FILE = "s3://nus-iss-group-3/cleaned_wiki.csv"

def get_mongo_client() -> pymongo.MongoClient:
	return pymongo.MongoClient(MONGO_HOST,
	                      username=MONGO_USER,
	                      password=MONGO_PASSWORD,
	                      authSource=MONGO_AUTH_SOURCE)

def load_documents_into_mongo(docu_search_database) -> None:
	mylist = []
	for i, chunk in enumerate(pd.read_csv(DOCUMENT_FILE, chunksize=CHUNK_SIZE)):
		print(f"Read chunk {i} which contains {chunk.size} rows")
		for index, row in chunk.iterrows():
			# print(row["topic"], row["content"])
			print(f"Insert row {index}", row["topic"])
			docu_search_database.documents.insert({
				"topic": row["topic"],
				"content": row["content"]})


if __name__ == "__main__":
	if argv[1] == "test":
		print("Test get params")
		print(MONGO_HOST, MONGO_USER, MONGO_PASSWORD, MONGO_AUTH_SOURCE)
		exit(0)
	else:
		client = get_mongo_client()
		db = client["docu_search"]
		collection = db.test_collection.find()
		print(collection[0])

		load_documents_into_mongo(docu_search_database=db)
		exit(0)

