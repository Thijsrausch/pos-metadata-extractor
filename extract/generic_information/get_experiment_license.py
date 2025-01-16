import os
from loguru import logger


def get_experiment_license(absolute_path_to_experiment, experiment_name):
    license_file_path = os.path.join(absolute_path_to_experiment, "LICENSE")

    if not os.path.isfile(license_file_path):
        logger.warning("LICENSE file not found in the repository")
        return

    with open(license_file_path, 'r') as file:
        first_line = file.readline().strip()

    relative_path = os.path.relpath(license_file_path, absolute_path_to_experiment)

    return {
        "license": first_line,
        "source": os.path.join(experiment_name, relative_path)
    }
