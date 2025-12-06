![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/ifaakash/ai_commit)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)


=========================================

 # Usage Steps:

1. Obtain your API Key:
   Register and get an **API** key from the DeepSeek AI developer dashboard.

2. Set the Environment Variable:
   Set your key as the <em>DEEPSEEK_API_KEY</em> environment variable.

   Example (for Linux/macOS):
   <em>export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxx"</em>

3. Install the Git Hook in your repository:
   Navigate to the root of any Git project and run the install command:
   <em>aicommitter install</em>

4. Commit!
   Stage your changes:
   <em>git add .</em>

   Commit directly with confirmation:
   <em>aicommitter generate --commit</em>

# Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## Latest Release

**Version 1.0.3** (2025-12-05)
- Updated the version of aicommitter to `1.0.3`
- Refactored exception handling
- Increased the session timeout to `180s` for <em>DEEPSEEK</em> and <em≥GEMINI</em>

For full details, see the [CHANGELOG](CHANGELOG.md).
