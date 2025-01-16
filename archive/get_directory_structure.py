import os


def get_directory_structure(absolute_path):
    directories = [d for d in os.listdir(absolute_path) if os.path.isdir(os.path.join(absolute_path, d))]

    return directories
