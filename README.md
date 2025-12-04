=========================================

 Usage Steps:

1. Obtain your API Key:
   Register and get an API key from the DeepSeek AI developer dashboard.

2. Set the Environment Variable:
   Set your key as the DEEPSEEK_API_KEY environment variable.

   Example (for Linux/macOS):
   export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxx"

3. Install the Git Hook in your repository:
   Navigate to the root of any Git project and run the install command:
   aicommitter install

4. Commit!
   Stage your changes:
   git add .

   Commit directly with confirmation:
   aicommitter generate --commit
