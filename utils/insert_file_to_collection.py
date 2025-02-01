from loguru import logger


def insert_json_to_mongodb(client, current_experiment, new_metadata, db_name, collection_name):
    db = client[db_name]

    collection = db[collection_name]

    if current_experiment:
        if current_experiment['version'] == new_metadata['version']:
            collection.replace_one({"experiment_name": current_experiment["experiment_name"]}, new_metadata)
            logger.info(f"Replaced JSON file data into {db_name}.{collection_name}")
            return

    collection.insert_one(new_metadata)
    logger.info(f"Inserted JSON file data into {db_name}.{collection_name}")
