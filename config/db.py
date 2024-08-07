from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config.settings import db_url, db_url2, db_name

def connect_to_database(url, database):
    client = MongoClient(url, server_api=ServerApi('1'))
    db = client[database]
    return client, db

# Connect to the first database
client1, db1 = connect_to_database(db_url, 'topic_modelling')

# Connect to the second database
client2, db2 = connect_to_database(db_url2, 'data_gathering')