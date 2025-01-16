def clone_and_list_folders(repo_url):
    # Get the directory where the Python script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Define the path where the repository will be cloned (inside the script's directory)
    repo_name = os.path.basename(repo_url).replace('.git', '')
    clone_path = os.path.join(script_dir, repo_name)

    # Clone the repository
    try:
        if os.path.exists(clone_path):
            print(f"Repository already exists in {clone_path}")
        else:
            print(f"Cloning repository from {repo_url} into {clone_path}")
            git.Repo.clone_from(repo_url, clone_path)
    except Exception as e:
        print(f"Error cloning repository: {e}")
        sys.exit(1)

    # List top-level directories in the cloned repository
    print("Top-level directories in the repository:")
    for item in os.listdir(clone_path):
        item_path = os.path.join(clone_path, item)
        if os.path.isdir(item_path):
            print(item)