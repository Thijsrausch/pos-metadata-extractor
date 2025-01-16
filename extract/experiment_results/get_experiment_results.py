import os
import glob
import csv
import re
from datetime import datetime
from loguru import logger


def get_experiment_results(absolute_path_to_repository, experiment_name):
    relative_path_to_results = os.path.join(experiment_name, "results")
    relative_path_to_data = os.path.join(experiment_name, "data")
    results_directory = os.path.join(absolute_path_to_repository, 'results')

    if not os.path.exists(results_directory):
        logger.warning(f"Results directory {results_directory} does not exist")
        return []

    try:
        experiment_results = []
        results_directory_names = [
            name
            for name in os.listdir(results_directory)
            if os.path.isdir(os.path.join(results_directory, name))
        ]

        for results_directory_name in results_directory_names:
            timestamp = format_dir_date(results_directory_name)
            data_directory = os.path.join(absolute_path_to_repository, "data")
            full_results_directory = os.path.join(results_directory, results_directory_name)
            data_files = find_files_with_timestamp(data_directory, timestamp)

            if not data_files:
                logger.warning(f"No data files found for timestamp {timestamp} in {data_directory}")
                continue

            result_data = []
            formatted_timestamp = datetime.strptime(timestamp, "%y%m%d_%H%M%S_%f").isoformat()
            for data_file in data_files:
                data = {
                    "source_file": os.path.join(relative_path_to_data, os.path.basename(data_file)),
                    "user": get_user_from_data_file(data_file),
                    "timestamp": formatted_timestamp,
                    "data": get_data_from_data_file(data_file)
                }
                result_data.append(data)

            result_metadata = {
                "timestamp": formatted_timestamp,
                "configuration": get_configuration_from_results_directory(full_results_directory, relative_path_to_results),
                "logging": get_logging_from_results_directory(full_results_directory, relative_path_to_results),
                "results_source": relative_path_to_results,
                "data_source": relative_path_to_data,
                "data": result_data
            }
            experiment_results.append(result_metadata)

        return experiment_results

    except Exception as e:
        logger.error(f"Error accessing results directory: {e}")
        return []


def find_files_with_timestamp(root_directory, timestamp):
    # Construct the pattern to match files containing the timestamp
    pattern = f"*{timestamp}*"
    search_path = os.path.join(root_directory, pattern)

    # Use glob to find all matching files
    matching_files = glob.glob(search_path)

    # Check if any files were found
    if not matching_files:
        logger.warning(f"No files found with timestamp {timestamp} in {root_directory}")
        return []
    return matching_files or None


def format_dir_date(dir_date):
    # # Original date string
    # date = "2020-10-07_23-22-39_868017"
    # Define the input format
    input_format = "%Y-%m-%d_%H-%M-%S_%f"
    # Define the target format
    target_format = "%y%m%d_%H%M%S_%f"

    # Parse the date string into a datetime object
    datetime_obj = datetime.strptime(dir_date, input_format)

    # Format the datetime object into the target string format
    return datetime_obj.strftime(target_format)


def get_user_from_data_file(data_file):
    # Extract just the filename from the full path
    filename = os.path.basename(data_file)
    
    # Split filename by '_' and get the first part which is the username
    username = filename.split('_')[0]
    return username


def get_data_from_data_file(data_file):
    data = []
    with open(data_file, 'r') as f:
        tsv_reader = csv.DictReader(f, delimiter='\t')
        for row in tsv_reader:
            # Convert string values to appropriate types
            typed_row = {}
            for key, value in row.items():
                # Handle space-separated values
                if ' ' in value:
                    # Split the value and key into parts
                    values = value.split()
                    keys = key.split()
                    
                    # Add each key-value pair
                    for i, (split_key, split_value) in enumerate(zip(keys, values)):
                        try:
                            typed_row[split_key] = float(split_value)
                        except ValueError:
                            typed_row[split_key] = split_value
                else:
                    try:
                        typed_row[key] = float(value)
                    except ValueError:
                        typed_row[key] = value
            data.append(typed_row)

    return data


def get_configuration_from_results_directory(results_directory_name, relative_path_to_results):
    # Get the config subdirectory path
    config_path = os.path.join(results_directory_name, 'config')
    if not os.path.exists(config_path):
        logger.warning(f"Config directory {config_path} does not exist")
        return {}

    config_data = {}
    try:
        # Find all JSON files in config directory
        json_files = glob.glob(os.path.join(config_path, '*.json'))
        
        if not json_files:
            logger.warning(f"No JSON files found in {config_path}")
            return {}

        # Load each JSON file into the dictionary
        import json
        for json_file in json_files:
            file_name = os.path.join(relative_path_to_results, os.path.basename(json_file))
            try:
                with open(json_file, 'r') as f:
                    config_data[file_name] = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from {file_name}: {e}")
                config_data[file_name] = {}
            except Exception as e:
                logger.error(f"Error reading {file_name}: {e}")
                config_data[file_name] = {}

        return config_data

    except Exception as e:
        logger.error(f"Error accessing config directory: {e}")
        return {}


def get_logging_from_results_directory(results_directory_name, relative_path_to_results):
    logging_data = {}
    try:
        # Get all subdirectories in results directory
        subdirs = [d for d in os.listdir(results_directory_name) 
                  if os.path.isdir(os.path.join(results_directory_name, d)) and d != 'config']
        
        # For each subdirectory (hostname), store the relative path
        for hostname in subdirs:
            relative_log_path = os.path.join(relative_path_to_results, hostname)
            logging_data[hostname] = relative_log_path

        return logging_data

    except Exception as e:
        logger.error(f"Error accessing logging directory: {e}")
        return {}

