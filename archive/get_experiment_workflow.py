import bashlex
import os
from loguru import logger


def get_experiment_workflow(absolute_path_to_experiment, file_name):
    # Construct the full path to the Bash script
    script_path = os.path.join(absolute_path_to_experiment, file_name)

    # Read the Bash script from the file
    try:
        with open(script_path, 'r') as file:
            bash_script = file.read()
    except FileNotFoundError:
        logger.warning(f"Error: The file '{script_path}' does not exist.")
        return None
    except Exception as e:
        logger.warning(f"Error reading the file '{script_path}': {e}")
        return None

    # Parse the script into a list of AST nodes
    try:
        parts = bashlex.parse(bash_script)
    except bashlex.errors.ParsingError as e:
        logger.error(f"Error parsing the Bash script: {e}")
        return None

    # Initialize metadata dictionary
    metadata = {
        "experiment": {
            "nodes": ["loadgen-experiment-node", "dut-experiment-node"],
            "images": [],
            "variable_files": {
                "loadgen": [],
                "dut": []
            },
            "scripts": {
                "setup": {
                    "loadgen": "",
                    "dut": ""
                },
                "measurement": {
                    "loadgen": "",
                    "dut": ""
                }
            },
            "execution_mode": ""
        },
        "resources": {
            "hosts": ["loadgen-experiment-node", "dut-experiment-node"],
            "operations": []
        },
        "artifacts": {
            "log_files": []
        }
    }

    # Node mapping
    node_mapping = {
        '"$1"': "loadgen-experiment-node",
        '"$2"': "dut-experiment-node"
    }

    def process_node(node):
        if node.kind == 'command':
            # Extract words from the command
            words = []
            for part in node.parts:
                if part.kind == 'word':
                    words.append(part.word)
            if words:
                cmd = words[0]
                args = words[1:]
                if cmd == 'pos' and args:
                    subcmd = args[0]
                    if subcmd == 'allocations' and len(args) > 1:
                        action = args[1]
                        if action in ['free', 'allocate']:
                            hosts = args[2:]
                            for host in hosts:
                                host_name = node_mapping.get(host, host)
                                if host_name not in metadata['resources']['hosts']:
                                    metadata['resources']['hosts'].append(host_name)
                            if action not in metadata['resources']['operations']:
                                metadata['resources']['operations'].append(action)
                        elif action == 'variables':
                            if len(args) > 3:
                                host = args[2]
                                var_file = args[3]
                                host_name = node_mapping.get(host, host)
                                flags = args[4:] if len(args) > 4 else []
                                if '--as-global' in flags:
                                    # Add to both nodes
                                    for node_key in ['loadgen', 'dut']:
                                        if var_file not in metadata['experiment']['variable_files'][node_key]:
                                            metadata['experiment']['variable_files'][node_key].append(var_file)
                                elif '--as-loop' in flags:
                                    if var_file not in metadata['experiment']['variable_files']['loadgen']:
                                        metadata['experiment']['variable_files']['loadgen'].append(var_file)
                                else:
                                    node_key = 'loadgen' if host_name == 'loadgen-experiment-node' else 'dut'
                                    if var_file not in metadata['experiment']['variable_files'][node_key]:
                                        metadata['experiment']['variable_files'][node_key].append(var_file)
                    elif subcmd == 'nodes' and len(args) > 1:
                        action = args[1]
                        if action == 'image':
                            if len(args) > 3:
                                image = args[3]
                                if image not in metadata['experiment']['images']:
                                    metadata['experiment']['images'].append(image)
                        elif action == 'reset':
                            if 'reboot' not in metadata['resources']['operations']:
                                metadata['resources']['operations'].append('reboot')
                    elif subcmd == 'commands' and len(args) > 1:
                        action = args[1]
                        if action == 'launch':
                            # Handle flags and infile
                            flags = args[2:]
                            infile = ''
                            host = ''
                            i = 0
                            while i < len(flags):
                                arg = flags[i]
                                if arg == '--infile' and i + 1 < len(flags):
                                    infile = flags[i + 1]
                                    i += 1
                                elif arg == '--loop':
                                    if metadata['experiment']['execution_mode'] != 'loop':
                                        metadata['experiment']['execution_mode'] = 'loop'
                                elif arg.startswith('--'):
                                    pass  # Skip other flags
                                else:
                                    host = arg
                                i += 1
                            host_name = node_mapping.get(host, host)
                            node_key = 'loadgen' if host_name == 'loadgen-experiment-node' else 'dut'
                            if infile:
                                if 'setup.sh' in infile:
                                    metadata['experiment']['scripts']['setup'][node_key] = infile
                                elif 'measurement.sh' in infile:
                                    metadata['experiment']['scripts']['measurement'][node_key] = infile
        # Recursively process child nodes
        for child in getattr(node, 'parts', []):
            process_node(child)
        for child in getattr(node, 'list', []):
            process_node(child)
        for child in getattr(node, 'commands', []):
            process_node(child)
        if hasattr(node, 'left'):
            process_node(node.left)
        if hasattr(node, 'right'):
            process_node(node.right)
        if hasattr(node, 'command'):
            process_node(node.command)
        if hasattr(node, 'then'):
            process_node(node.then)
        if hasattr(node, 'else_'):
            process_node(node.else_)
        if hasattr(node, 'body'):
            process_node(node.body)

    for part in parts:
        process_node(part)

    # Generate log files based on script names
    for script_type in ['setup', 'measurement']:
        for node_type in ['loadgen', 'dut']:
            script_name = metadata['experiment']['scripts'][script_type][node_type]
            if script_name:
                log_file = script_name.replace('.sh', '.log')
                if log_file not in metadata['artifacts']['log_files']:
                    metadata['artifacts']['log_files'].append(log_file)

    return metadata
