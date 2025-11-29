Follow below commands to make this work

STEP 1:
Depending on you LLM agent, set the API key

export DEEPSEEK_API_KEY="sk-..."
# or
export GEMINI_API_KEY="sk-..."

STEP 2:
alias aicommitter="aicommit"

STEP 3:
aicommit install

STEP 4:
git add .

STEP 5:
aicommit generate --commit

==========================================

If you are one MAC, you can permanently set the API key on your ZSH ( Z shell )
- vi ~/.zshrc
- Create alias using `alias key="value"`
- Save and run  `source ~/.zshrc`

==========================================

Optional: Pick the LLM provider explicitly ( not mandatory, feel free to skip )

You can set the LLM for the tool using the below command

`aicommitter generate --provider <name_of_LLM>` 
eg, `aicommitter generate --provider deepseek`.

Just make sure the relevant API key (DEEPSEEK_API_KEY or GEMINI_API_KEY) is set in your environment beforehand.
