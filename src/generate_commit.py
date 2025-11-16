import os
import subprocess
import sys

import requests
from dotenv import load_dotenv

# --- Configuration ---
# Use environment variables for flexibility
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-reasoner")

# 1. Initialize a requests Session object at the module level
# This object will be reused for all requests to the same host.
SESSION = requests.Session()


def get_diff() -> str:
    """Runs 'git diff --cached' and handles subprocess errors."""
    try:
        # check=True raises an exception on non-zero exit code
        diff = subprocess.run(
            ["git", "diff", "--cached"], capture_output=True, text=True, check=True
        )
        return diff.stdout
    except subprocess.CalledProcessError as e:
        sys.stderr.write(
            f"ERROR: Git command failed. Is this a Git repo? Details: {e.stderr.strip()}\n"
        )
        return ""
    except FileNotFoundError:
        sys.stderr.write(
            "ERROR: 'git' command not found. Ensure Git is in your PATH.\n"
        )
        return ""


def generate_message(git_diff: str) -> str:
    """Calls the DeepSeek API using the shared session to generate a commit message."""

    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        sys.stderr.write(
            "ERROR: API key not found. Please set the DEEPSEEK_API_KEY environment variable.\n"
        )
        return ""

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    prompt = f"""
    You are a helpful assistant that writes concise Git commit messages.
    Write a commit message that describes the following diff.
    The message must follow the Conventional Commit format (e.g., feat: added new endpoint).

    Diff:
    {git_diff}
    """

    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "system", "content": prompt}],
        "stream": False,
    }

    try:
        # 2. Use SESSION.post() instead of requests.post()
        # This reuses the underlying connection if possible.
        response = SESSION.post(url, headers=headers, json=data, timeout=120)

        # Raise HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()

        result = response.json()

        # Extract message content
        message = (
            result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        )

        if not message:
            sys.stderr.write(
                "ERROR: API response was successful but returned no message content.\n"
            )
            return ""

        return message

    except requests.exceptions.RequestException as e:
        sys.stderr.write(f"ERROR: API request failed. Network or HTTP Error: {e}\n")
        return ""


if __name__ == "__main__":
    # Load environment variables once at the start
    load_dotenv()

    diff = get_diff()

    if not diff.strip():
        # Only print status if there's no diff, otherwise it pollutes the output
        sys.stderr.write(
            "INFO: No staged changes found. Commit message will be empty.\n"
        )
        # Exit silently so the hook doesn't necessarily abort the commit if it's fine to proceed
        # but in a pre-commit context, often you want to abort if there's no diff.
        # We rely on the shell script to check the final output.
        print("")  # Print empty string to STDOUT
        exit(0)

    commit_message = generate_message(diff)

    # Print the final, clean message to STDOUT for the hook to capture
    print(commit_message)

    # 3. Explicitly close the session's underlying connections when done
    SESSION.close()
