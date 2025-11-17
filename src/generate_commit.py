import os
import subprocess
import sys
from subprocess import DEVNULL

import requests
import typer
from dotenv import load_dotenv

# Initialize Typer App
app = typer.Typer(
    help="AI Commit Message Generator. Reads staged Git diff and suggests a message"
)

# Initialize requests Session object globally for connection reuse
SESSION = requests.Session()


# --- Utility Functions ---
def get_diff() -> str:
    """Runs 'git diff --cached' and handles errors."""
    try:
        # 1. First subprocess.run: Check if we are inside a Git repository
        # Use stdout=DEVNULL and stderr=DEVNULL instead of capture_output=True
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=DEVNULL,  # Discard stdout
            stderr=DEVNULL,  # Discard stderr
            check=True,  # Raise CalledProcessError if not in a git repo
        )

        # 2. Second subprocess.run: Get the actual diff
        # Here, you DO want to capture output, so use capture_output=True
        diff = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,  # Captures stdout and stderr
            text=True,  # Decodes output to string
            check=True,
        )
        return diff.stdout
    except subprocess.CalledProcessError:
        typer.echo("Error: Git command failed. Are you in a Git repository?", err=True)
        return ""
    except FileNotFoundError:
        typer.echo(
            "Error: 'git' command not found. Ensure Git is in your PATH.", err=True
        )
        return ""


def generate_message(git_diff: str, api_key: str, model_name: str) -> str:
    """Calls the DeepSeek API to generate a commit message"""

    if not api_key:
        typer.echo(
            "Error: API key not set. Set DEEPSEEK_API_KEY environment variable.",
            err=True,
        )
        return ""

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    prompt = f"""
    You are a helpful assistant that writes concise Git commit messages.
    Write a commit message that describes the following diff, following Conventional Commit format.

    Diff:
    {git_diff}
    """

    data = {
        "model": model_name,
        "messages": [{"role": "system", "content": prompt}],
        "stream": False,
    }

    try:
        # Use the global session object with a generous timeout
        typer.echo("... Calling AI model for generation (This may take up to 60s) ...")
        response = SESSION.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        result = response.json()
        message = (
            result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        )

        if not message:
            typer.echo("Error: API returned no message content.", err=True)
            return ""

        return message

    except requests.exceptions.RequestException as e:
        typer.echo(f"Error: API request failed. Network or HTTP Error: {e}", err=True)
        return ""


# --- Main Typer Command ---
@app.command(name="generate")
def cli_generate(
    commit: bool = typer.Option(
        False,
        "--commit",
        "-c",
        help="Immediately commit the suggested message if confirmed.",
    ),
    api_key: str = typer.Option(
        ...,  # Ellipsis indicates required if not provided by envvar
        hidden=True,  # Hide this in --help for security, rely on envvar
        envvar="DEEPSEEK_API_KEY",
    ),
    model: str = typer.Option(
        "deepseek-reasoner",
        "--model",
        "-m",
        envvar="DEEPSEEK_MODEL",
        help="DeepSeek model to use.",
    ),
):
    """
    Generates a Conventional Commit message from staged Git changes.
    """

    diff = get_diff()

    if not diff.strip():
        typer.echo("INFO: No staged changes found. Commit message will be empty.")
        raise typer.Exit(code=0)

    # Generate message
    commit_message = generate_message(diff, api_key, model)

    if not commit_message:
        raise typer.Exit(code=1)

    typer.echo("\n" + "=" * 50)
    typer.echo("Suggested Commit Message:")
    typer.echo(commit_message)
    typer.echo("=" * 50 + "\n")

    if commit:
        # Interactive confirmation
        confirm = typer.confirm("Do you want to use this message to commit?")
        if confirm:
            try:
                # Use Git to commit the message
                subprocess.run(["git", "commit", "-m", commit_message], check=True)
                typer.echo(
                    typer.style("Commit successful!", fg=typer.colors.GREEN, bold=True)
                )
            except subprocess.CalledProcessError:
                typer.echo(
                    "Error: Git commit failed. Check status for details.", err=True
                )
                raise typer.Exit(code=1)
        else:
            typer.echo("Commit aborted by user.")
            raise typer.Exit()
    else:
        typer.echo("Message generated. Run with '-c' to commit automatically.")


if __name__ == "__main__":
    # Load .env file variables before running the application
    load_dotenv(override=True)
    try:
        app()
    finally:
        SESSION.close()
