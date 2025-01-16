import os
import yaml


def get_experiment_nodes(absolute_path_to_experiment, experiment_name):
    experiment_directory = absolute_path_to_experiment + "/experiment"
    subdirs = [d for d in os.listdir(experiment_directory) if os.path.isdir(os.path.join(experiment_directory, d))]

    nodes = []
    for subdir in subdirs:
        subdir_path = os.path.join(experiment_directory, subdir)
        if os.path.isdir(subdir_path):
            node = {
                'role': os.path.basename(subdir_path),
                'source': experiment_name + '/experiment/' + os.path.basename(subdir_path),
                'variables': get_global_variables(subdir_path),
                'setup_script': get_setup_script(subdir_path, experiment_name),
                'measurement_script': get_measurement_script(subdir_path, experiment_name),
            }
            nodes.append(node)

    return nodes


def get_global_variables(subdir_path):
    global_vars_path = os.path.join(subdir_path, 'variables.yml')
    with open(global_vars_path, 'r') as f:
        global_vars = yaml.safe_load(f)
        return global_vars if global_vars else {}


def get_setup_script(subdir_path, experiment_name):
    setup_script_path = os.path.join(subdir_path, 'setup.sh')

    return {
        'source': experiment_name + '/experiment/' + os.path.basename(subdir_path) + '/setup.sh',
        'script_type': 'setup',
        'language': get_script_language(setup_script_path)
    }


def get_measurement_script(subdir_path, experiment_name):
    measurement_script_path = os.path.join(subdir_path, 'measurement.sh')

    return {
        'source': experiment_name + '/experiment/' + os.path.basename(subdir_path) + '/measurement.sh',
        'script_type': 'measurement',
        'language': get_script_language(measurement_script_path)
    }


def is_bash_script(script):
    """Determines if the script is a Bash script."""
    lines = script.strip().split("\n")

    # Check for shebang
    if lines and lines[0].startswith("#!"):
        if "bash" in lines[0]:
            return True
    return False


def get_script_language(script):
    """Determines the language of the script."""
    try:
        with open(script, 'r') as f:
            script_content = f.read()
        
        if is_bash_script(script_content):
            return 'bash'
        return 'unknown'
    except FileNotFoundError:
        return 'unknown'
    except Exception:
        return 'unknown'

