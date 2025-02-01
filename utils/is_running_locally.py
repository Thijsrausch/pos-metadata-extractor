import os


def is_running_locally():
    return os.getenv('ACTION') != 'true'
