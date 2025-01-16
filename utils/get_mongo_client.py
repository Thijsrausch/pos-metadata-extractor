from pymongo import MongoClient, errors
from loguru import logger


def get_local_mongo_client(host, port):
    if not isinstance(port, int):
        try:
            port = int(port)
        except ValueError:
            logger.error("The string is not a valid integer.")

    return MongoClient(host, port)


def get_mongo_client(mongo_uri):
    try:
        client = MongoClient(mongo_uri)
        # Test the connection (optional, but recommended)
        client.admin.command('ping')
        print("MongoDB connection established.")
        return client
    except errors.ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
    except errors.InvalidURI as e:
        print(f"Invalid MongoDB URI: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None
