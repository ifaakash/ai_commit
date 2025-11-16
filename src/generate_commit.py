import os
import subprocess

import requests
from dotenv import load_dotenv


def get_diff():
    try:
        # Added check=True to raise an exception on non-zero exit code
        diff = subprocess.run(
            ["git", "diff", "--cached"], capture_output=True, text=True, check=True
        )
        return diff.stdout
    except subprocess.CalledProcessError as e:
        print(
            f"Error running 'git diff --cached'. Is this a Git repository? Details: {e.stderr.strip()}"
        )
        return ""
    except FileNotFoundError:
        print(
            "Error: 'git' command not found. Ensure Git is installed and in your PATH."
        )
        return ""


def generate_message(git_diff: str):
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        print(
            "API key not found. Please set the DEEPSEEK_API_KEY environment variable."
        )
        return ""

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    prompt = f"""
    You are a helpful assistant that writes concise Git commit messages.

    Write a commit message that describes the following diff:

    {git_diff}
    """

    # Call AI model to generate commit message
    data = {
        "model": "deepseek-reasoner",  # Use 'deepseek-reasoner' for R1 model or 'deepseek-chat' for V3 model
        "messages": [{"role": "system", "content": prompt}],
        "stream": False,  # Disable streaming
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        message = result["choices"][0]["message"]["content"]
    else:
        print("Request failed, error code:", response.status_code)
        message = ""

    return message


if __name__ == "__main__":
    # Call the environment variable loader function
    load_dotenv()

    commit_message = ""

    # Call the function to fetch the difference from the last commit
    diff = get_diff()
    print(diff)

    if not diff.strip():
        commit_message = "No staged changes. Commit message will be empty"
        exit(0)
    else:
        # If difference is not empty, generate the commit message
        commit_message = generate_message(diff)

    print(commit_message)
