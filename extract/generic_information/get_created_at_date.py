import git
from loguru import logger


def get_created_at_date(repo_path):
    """
    Retrieves the date and commit ID (SHA) of the first (oldest) commit in the repository.

    Parameters:
    - repo_path (str): The file system path to the local Git repository.

    Returns:
    - first_commit_date (str): The date of the first commit, in 'YYYY-MM-DD HH:MM:SS' format.
    - first_commit_sha (str): The commit ID (SHA) of the first commit.
    """
    try:
        repo = git.Repo(repo_path)
        # Obtain the oldest commit from HEAD by iterating in reverse
        first_commit = next(repo.iter_commits('HEAD', reverse=True))
        first_commit_date = first_commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return first_commit_date
    except StopIteration:
        # This happens if the repository has no commits
        logger.error("No commits found in the repository.")
        return None, None
    except Exception as e:
        logger.error(f"An error occurred while getting the first commit info: {e}")
        return None, None
