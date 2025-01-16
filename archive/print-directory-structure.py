import os


def print_directory_structure(start_path, level=0):
    # Print the directory name with indentation based on level
    print("    " * level + os.path.basename(start_path) + "/")

    # Get subdirectories
    for item in os.listdir(start_path):
        item_path = os.path.join(start_path, item)
        # If item is a directory, recursively call the function
        if os.path.isdir(item_path):
            print_directory_structure(item_path, level + 1)


# Specify your directory path
start_path = '../../pos-artifacts'
print_directory_structure(start_path)
