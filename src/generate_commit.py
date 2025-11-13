import subprocess
from pydoc import text


def get_diff():
    diff = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return diff.stdout


def generate_message(git_diff: str):
    return 0


if __name__ == "__main__":
    diff = get_diff()

    if not diff.strip():
        print("No staged changes. Commit message will be empty.")
        exit(0)

    commit_message = generate_message(diff)
