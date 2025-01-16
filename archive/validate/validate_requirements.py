import os


def check_files_and_folder_structure(current_dir, structure):
    missing_items = []

    for item, item_type in structure.items():
        item_path = os.path.join(current_dir, item)

        if item_type == 'folder':
            if not os.path.isdir(item_path):
                missing_items.append(f"Missing folder: {item_path}")
            else:
                # Recursively check sub-folders
                check_files_and_folder_structure(item_path, structure[item])

        elif item_type == 'file':
            if not os.path.isfile(item_path):
                missing_items.append(f"Missing file: {item_path}")

    return missing_items


def validate_requirements(root_dir):
    expected_structure = {
        "VERSION": "file",
        "LICENSE": "file",
    }

    missing_items = check_files_and_folder_structure(root_dir, expected_structure)

    # TODO - check file contents?
    # TODO -

    is_valid = len(missing_items) == 0
    return is_valid, missing_items
