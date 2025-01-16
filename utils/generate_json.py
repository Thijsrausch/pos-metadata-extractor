import json
from loguru import logger


def generate_json(dictionary, title):
    try:
        json_data = json.dumps(dictionary, ensure_ascii=False, indent=4)
        logger.info(f"JSON file has been generated")
        return json_data

    except Exception as e:
        logger.error(f"An error occurred while generating JSON: {e}")
