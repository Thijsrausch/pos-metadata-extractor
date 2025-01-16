import os
import yaml
from loguru import logger


def get_loop_variables(experiment_directory):
    try:
        loop_vars_path = os.path.join(experiment_directory, 'loop-variables.yml')
        if not os.path.exists(loop_vars_path):
            logger.warning(f"Loop variables file {loop_vars_path} does not exist")
            return None
            
        with open(loop_vars_path, 'r') as f:
            loop_vars = yaml.safe_load(f)
            return loop_vars if loop_vars else {}
            
    except Exception as e:
        logger.error(f"Error accessing loop variables: {e}")
        return None