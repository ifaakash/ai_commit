# import importlib.resources
# import os
# import subprocess
# import sys
# from pathlib import Path
# from subprocess import DEVNULL

# import requests
# import typer
# from dotenv import load_dotenv

# # Load .env file variables before running the application
# load_dotenv(override=True)

# # Initialize Typer App
# app = typer.Typer(
#     help="AI Commit Message Generator. Reads staged Git diff and suggests a message"
# )

# # Initialize requests Session object globally for connection reuse
# SESSION = requests.Session()

# # --- NEW Hook Installation Command ---

# # Multiline string containing the content of your shell script (Step 1)
# HOOK_SCRIPT_CONTENT = """#!/usr/bin/env bash
# COMMIT_MSG_FILE=$1
# echo "--- Prepare-Commit-Message Hook Triggered ---" > /dev/tty
# cd "$(git rev-parse --show-toplevel)" || exit 1
# EXISTING_MSG=$(grep -v '^#' "$COMMIT_MSG_FILE" | head -n 1 | tr -d '[:space:]')
# if [[ -n "$EXISTING_MSG" ]]; then
#     echo "INFO: User provided an existing message. Skipping AI generation." > /dev/tty
#     exit 0
# fi
# set -e
# GENERATED_MSG=$(aicommitter generate)
# set +e
# if [[ -z "$(echo "$GENERATED_MSG" | tr -d '[:space:]')" ]]; then
#     echo "ERROR: Generated message is empty. Manual edit required." > /dev/tty
#     exit 1
# fi
# echo "$GENERATED_MSG" > "$COMMIT_MSG_FILE"
# echo "INFO: Successfully generated and set the commit message." > /dev/tty
# echo "--- Generated Message ---" > /dev/tty
# echo "$GENERATED_MSG" > /dev/tty
# echo "-------------------------" > /dev/tty
# exit 0
# """


# # def get_readme(filepath: str = "docs.md") -> str:
# #     """Read the docs.md and return to user"""
# #     try:
# #         with open(filepath, "r", encoding="utf-8") as f:
# #             return f.read()
# #     except FileNotFoundError:
# #         return typer.style(
# #             f"Error: Documentation file '{filepath}' not found in the current directory.",
# #             fg=typer.colors.REDs,
# #         )
# #     except Exception as e:
# #         return typer.style(
# #             f"Error reading documentation file: {e}", fg=typer.colors.RED
# #         )


# def get_readme_content(filepath: str = "docs.md") -> str:
#     """
#     Reads the content of the README file from the installed Python package resources.

#     The file must be bundled within the 'aicommitter' package (e.g., inside src/aicommitter/).
#     """

#     try:
#         # 1. Try reading the resource from the installed package
#         # Assuming the main package is named 'generate_commit'
#         return importlib.resources.read_text("aicommitter", filepath)

#     except FileNotFoundError:
#         # 3. If that fails too, inform the user
#         return typer.style(
#             f"Error: Documentation file '{filepath}' not found. Please ensure it is either in the project root (dev mode) or packaged as a resource inside the 'aicommitter' package (installed mode).",
#             fg=typer.colors.RED,
#         )
#     except Exception as e:
#         # Handle other packaging/read errors
#         return typer.style(
#             f"Error reading documentation file from package resource: {e}",
#             fg=typer.colors.RED,
#         )


# @app.command(name="docs")
# def show_docs():
#     """Displays the full project documentation from README.md"""
#     readme_content = get_readme_content()
#     typer.echo(typer.style(f"\n{readme_content}", fg=typer.colors.GREEN, italic=True))


# @app.command(name="install")
# def install_hook():
#     """Installs the prepare-commit-msg hook in the current Git repository."""
#     try:
#         # Check if we are in a Git repository
#         git_dir = subprocess.run(
#             ["git", "rev-parse", "--git-dir"],
#             capture_output=True,
#             check=True,
#             text=True,
#         ).stdout.strip()

#         hook_path = os.path.join(git_dir, "hooks", "prepare-commit-msg")

#         with open(hook_path, "w") as f:
#             f.write(HOOK_SCRIPT_CONTENT)

#         # Make the hook executable
#         os.chmod(hook_path, 0o755)

#         typer.echo(
#             typer.style(
#                 f"\nSuccessfully installed hook in {hook_path}",
#                 fg=typer.colors.GREEN,
#                 bold=True,
#             )
#         )
#         typer.echo("Run 'git commit' in this repository to test.")

#     except subprocess.CalledProcessError:
#         typer.echo(
#             typer.style(
#                 "ERROR: Not in a Git repository. Installation aborted.",
#                 fg=typer.colors.RED,
#             ),
#             err=True,
#         )
#         raise typer.Exit(code=1)


# # --- Utility Functions ---
# def get_diff() -> str:
#     """Runs 'git diff --cached' and handles errors."""
#     try:
#         # 1. First subprocess.run: Check if we are inside a Git repository
#         # Use stdout=DEVNULL and stderr=DEVNULL instead of capture_output=True
#         subprocess.run(
#             ["git", "rev-parse", "--is-inside-work-tree"],
#             stdout=DEVNULL,  # Discard stdout
#             stderr=DEVNULL,  # Discard stderr
#             check=True,  # Raise CalledProcessError if not in a git repo
#         )

#         # 2. Second subprocess.run: Get the actual diff
#         # Here, you DO want to capture output, so use capture_output=True
#         diff = subprocess.run(
#             ["git", "diff", "--cached"],
#             capture_output=True,  # Captures stdout and stderr
#             text=True,  # Decodes output to string
#             check=True,
#         )
#         return diff.stdout
#     except subprocess.CalledProcessError:
#         typer.echo("Error: Git command failed. Are you in a Git repository?", err=True)
#         return ""
#     except FileNotFoundError:
#         typer.echo(
#             "Error: 'git' command not found. Ensure Git is in your PATH.", err=True
#         )
#         return ""


# def generate_message(git_diff: str, api_key: str, model_name: str) -> str:
#     """Calls the DeepSeek API to generate a commit message"""

#     if not api_key:
#         typer.echo(
#             "Error: API key not set. Set DEEPSEEK_API_KEY environment variable.",
#             err=True,
#         )
#         return ""

#     url = "https://api.deepseek.com/chat/completions"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {api_key}",
#     }

#     prompt = f"""
#     You are a helpful assistant that writes concise Git commit messages.
#     Write a commit message that describes the following diff, following Conventional Commit format.

#     Diff:
#     {git_diff}
#     """

#     data = {
#         "model": model_name,
#         "messages": [{"role": "system", "content": prompt}],
#         "stream": False,
#     }

#     try:
#         # Use the global session object with a generous timeout
#         typer.echo("... Calling AI model for generation (This may take up to 60s) ...")
#         response = SESSION.post(url, headers=headers, json=data, timeout=60)
#         response.raise_for_status()

#         result = response.json()
#         message = (
#             result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
#         )

#         if not message:
#             typer.echo("Error: API returned no message content.", err=True)
#             return ""

#         return message

#     except requests.exceptions.RequestException as e:
#         typer.echo(f"Error: API request failed. Network or HTTP Error: {e}", err=True)
#         return ""


# # --- Main Typer Command ---
# @app.command(name="generate")
# def cli_generate(
#     commit: bool = typer.Option(
#         False,
#         "--commit",
#         "-c",
#         help="Immediately commit the suggested message if confirmed.",
#     ),
#     # api_key: str = typer.Option(
#     #     ...,  # Ellipsis indicates required if not provided by envvar
#     #     hidden=True,  # Hide this in --help for security, rely on envvar
#     #     envvar="DEEPSEEK_API_KEY",
#     #     help="API key for the provider (DeepSeek or Gemini).",
#     # ),
#     api_key: str = typer.Option(
#         False,
#         "--api-key",
#         "-c",
#         hidden=True,
#         help="API key for the provider (DeepSeek or Gemini).",
#     ),
#     model: str = typer.Option(
#         "deepseek-reasoner",
#         "--model",
#         "-m",
#         envvar="DEEPSEEK_MODEL",
#         help="DeepSeek model to use.",
#     ),
# ):
#     """
#     Generates a Conventional Commit message from staged Git changes.
#     """

#     diff = get_diff()

#     if not diff.strip():
#         typer.echo("INFO: No staged changes found. Commit message will be empty.")
#         raise typer.Exit(code=0)

#     # Generate message
#     commit_message = generate_message(diff, api_key, model)

#     if not commit_message:
#         raise typer.Exit(code=1)

#     typer.echo("\n" + "=" * 50)
#     typer.echo("Suggested Commit Message:")
#     typer.echo(commit_message)
#     typer.echo("=" * 50 + "\n")

#     if commit:
#         # Interactive confirmation
#         confirm = typer.confirm("Do you want to use this message to commit?")
#         if confirm:
#             try:
#                 # Use Git to commit the message
#                 subprocess.run(["git", "commit", "-m", commit_message], check=True)
#                 typer.echo(
#                     typer.style("Commit successful!", fg=typer.colors.GREEN, bold=True)
#                 )
#             except subprocess.CalledProcessError:
#                 typer.echo(
#                     "Error: Git commit failed. Check status for details.", err=True
#                 )
#                 raise typer.Exit(code=1)
#         else:
#             typer.echo("Commit aborted by user.")
#             raise typer.Exit()
#     else:
#         typer.echo("Message generated. Run with '-c' to commit automatically.")


# if __name__ == "__main__":
#     try:
#         app()
#     finally:
#         SESSION.close()
