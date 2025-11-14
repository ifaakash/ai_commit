import subprocess
from pydoc import text

import requests


def get_diff():
    diff = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return diff.stdout


def generate_message(git_diff: str):
    prompt = f"""
    You are a helpful assistant that writes concise Git commit messages.

    Write a commit message that describes the following diff:

    {git_diff}
    """

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer ${{secrets.API_KEY}}",
    }

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
    diff = get_diff()

    if not diff.strip():
        print("No staged changes. Commit message will be empty.")
        exit(0)

    commit_message = generate_message(diff)
    print(commit_message)
