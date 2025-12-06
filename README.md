![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/ifaakash/ai_commit)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Latest Release](https://img.shields.io/badge/Release-1.0.3-orange)
<!--[![Latest Release](https://img.shields.io/badge/Latest-Release-blue?style=for-the-badge)](https://libraries.io/pypi/aicommitter)-->

### One-Time Setup

1. **Obtain your API Key**  
   Register and get an API key from the DeepSeek AI developer dashboard<br>
   - Get DeepSeek API key from [Deepseek Dashboard](https://platform.deepseek.com/api_keys)
   - Get Gemini API key from [Gemini Dashboard](https://aistudio.google.com/api-keys)

2. **Set the Environment Variable**  
   Set your key as the DEEPSEEK_API_KEY environment variable<br>
   ```bash
   export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxx"
   ```

3. **Install the Git Hook in your repository**  
   Navigate to the root of any Git project and run the install command<br>
   ```bash
   aicommitter install
   ```

### Daily Usage
For every commit after setup:

4. **Stage your changes**  
   Add all or selected changes to the staging area<br>
   ```bash
   git add .
   ```

5. **Commit!**  
   Commit directly with confirmation<br>
   ```bash
   aicommitter generate --commit
   ```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a [detailed history](https://libraries.io/pypi/aicommitter) of changes

## Latest Release

**Version 1.0.3** (2025-12-05)
- Updated the version of aicommitter to `1.0.3`
- Refactored exception handling
- Increased the session timeout to `180s` for `DEEPSEEK` and `GEMINI`

For full details, see the [CHANGELOG](CHANGELOG.md).
