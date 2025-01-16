import os
import yaml
from loguru import logger


def get_global_variables(experiment_directory):
    try:
        global_vars_path = os.path.join(experiment_directory, 'global-variables.yml')
        if not os.path.exists(global_vars_path):
            logger.warning(f"Global variables file {global_vars_path} does not exist")
            return None
            
        with open(global_vars_path, 'r') as f:
            global_vars = yaml.safe_load(f)
            return global_vars if global_vars else {}
            
    except Exception as e:
        logger.error(f"Error accessing global variables: {e}")
        return None