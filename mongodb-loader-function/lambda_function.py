import codecs
import csv
import urllib.parse
import logging
import sys
import boto3
import pymongo


logging.info('Loading function MongoDBLoader')

# Prepare calls to the AWS API
# S3
s3 = boto3.client('s3')
# Systems Manager
ssm = boto3.client('ssm')

# Secrets
MONGO_HOST=ssm.get_parameter(Name="/prod/mongodb/host", WithDecryption=True)['Parameter']['Value']
MONGO_USER=ssm.get_parameter(Name="/prod/mongodb/username", WithDecryption=True)['Parameter']['Value']
MONGO_PASSWORD=ssm.get_parameter(Name="/prod/mongodb/password", WithDecryption=True)['Parameter']['Value']
MONGO_AUTH_SOURCE=ssm.get_parameter(Name="/prod/mongodb/auth_source", WithDecryption=True)['Parameter']['Value']

# Log to stdout to make logs appear in CloudWatch
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def get_mongo_client() -> pymongo.MongoClient:
    return pymongo.MongoClient(MONGO_HOST,
                          username=MONGO_USER,
                          password=MONGO_PASSWORD,
                          authSource=MONGO_AUTH_SOURCE)
                          
def test_mongo_cursor():
    client = get_mongo_client()
    db = client["docu_search"]
    collection = db.test_collection.find()
    logging.debug(collection[0])
    
    return

def load_documents_into_mongo(docu_search_database: pymongo.database.Database, bucket_name: str, key: str) -> int:
    logging.info("Reading s3://%s/%s", bucket_name, key)
    rows_loaded = 0
    
    data = s3.get_object(Bucket=bucket_name, Key=key)

    for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"])):
        docu_search_database.documents.insert({"topic": row["topic"], "content": row["content"]})
        rows_loaded += 1

    return rows_loaded

def main(event, context):
    logging.info("Hello there")
    
    logging.debug("%s %s %s %s", MONGO_HOST, MONGO_USER, MONGO_PASSWORD, MONGO_AUTH_SOURCE)
    test_mongo_cursor()

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        logging.info(f"Reading the object s3://{bucket}/{key}")
        response = s3.get_object(Bucket=bucket, Key=key)
        logging.info("CONTENT TYPE: " + response['ContentType'])

        client = get_mongo_client()
        db = client["docu_search"]
        rows_loaded = load_documents_into_mongo(docu_search_database=db, bucket_name=bucket, key=key)

        return f"Loaded s3://{bucket}/{key} containing {rows_loaded} rows into MongoDB"

    except Exception as e:
        logging.error(e)
        logging.error('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
