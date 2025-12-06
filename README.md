![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/ifaakash/ai_commit)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

 ## Usage Steps:

1. Obtain your API Key:<br>
   Register and get an **API** key from the DeepSeek AI developer dashboard.

2. Set the Environment Variable:<br>
   Set your key as the **DEEPSEEK_API_KEY** environment variable.

   Example (for Linux/macOS):<br>
   `export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxx"`

3. Install the Git Hook in your repository:<br>
   Navigate to the root of any Git project and run the install command:
   `aicommitter install`

4. Commit!
   Stage your changes:<br>
   `git add .`

   Commit directly with confirmation:<br>
   `aicommitter generate --commit`

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## Latest Release

**Version 1.0.3** (2025-12-05)
- Updated the version of aicommitter to `1.0.3`
- Refactored exception handling
- Increased the session timeout to `180s` for `DEEPSEEK` and `GEMINI`

For full details, see the [CHANGELOG](CHANGELOG.md).
