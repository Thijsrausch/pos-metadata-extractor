import os


def has_dut_folder(root_directory):
    # Define the expected dut path
    dut_path = os.path.join(root_directory, "experiment", "dut")

    # Check if the path exists and is a directory
    return os.path.isdir(dut_path)