import dotenv
import os
from pymongo import MongoClient
from listentweet.settings import PROJECT_DIR


def get_mongo_auth_from_env():
    dotenv_path = os.path.join(PROJECT_DIR, ".env")
    dotenv.load_dotenv(dotenv_path)
    mongo_host = os.getenv("MONGO_HOST")
    if not mongo_host:
        raise OSError(
            """`MONGO_HOST` not found in enviroment.
            Please add `MONGO_HOST=mongodb://YOUR_MONGO_DB_SERVERIP:MONGO_PORT` to .env.
            Or declare before the execution.
        """
        )
    return mongo_host


def init_mongo_client():
    mongo_host = get_mongo_auth_from_env()
    mongo_client = MongoClient(mongo_host)
    return mongo_client


def init_collection_of_database(db_name, collection_name):
    mongo_client = init_mongo_client()
    collection = mongo_client.get_database(db_name).get_collection(
        collection_name
    )
    return collection
