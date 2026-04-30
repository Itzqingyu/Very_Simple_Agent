# Very Simple Agent
[English](README.md) | [繁體中文](README.zh-TW.md)

---
This is a lightweight, progressive AI Agent project implemented in Python.
The project demonstrates how to evolve from a basic API call to an autonomous Agent with a beautiful CLI interface and the ability to execute local command-line operations step by step.

## ✨ Core Features
---
*   **Progressive Learning Architecture**: From `Agent1.py` to `Agent5.py`, demonstrating the iterative process of Agent functionalities.
*   **Local System Command Execution**: The Agent can parse conversational intents, generate and execute local terminal (bash/cmd) commands via `subprocess`, and capture correct outputs and system errors, achieving real interaction with the local environment.
*   **Beautiful CLI Interface**: Uses the `rich` library to build a high-quality interactive interface in the terminal, including prompt panels, color highlights, and separators.
*   **Token & Cost Tracking**: Features token consumption recording and API cost calculation (`Agent5.py`).
*   **Externalized Prompts**: The System Prompt is stored independently in `system_prompt.md`, making it easy to adjust the Agent's role settings and behavioral guidelines at any time.
*   **Multi-Model Support**: In addition to supporting the official OpenAI API, `Agent_openrouter.py` provides an example of how to connect to OpenRouter to use other open-source models (like Gemma, etc.).

## 🗂️ Project Structure & Version History
---
This project has gone through several important version iterations (refer to the Git Log):
1. **Initialization & Basic Connection**: Created the base directory, set up `.gitignore`, and completed basic OpenAI and OpenRouter connections.
2. **Refactoring System Prompt**: Extracted the hardcoded prompt from the code into an independent `system_prompt.md`.
3. **Optimizing CLI & System Interaction**: Refactored the code structure in the latest scripts, added the `rich` interface, and improved the system command execution and error (`stderr`) capturing mechanisms.
4. **Progressive Feature Integration**: Split into `Agent1.py` ~ `Agent5.py` to fully record the evolution of features.

### 🕵️ Agent Evolution Analysis
*   **`Agent1.py`**: The most basic connection. Reads the key from `.env` and uses `gpt-4o-mini` for a Q&A conversation loop.
*   **`Agent2.py`**: Adds **System Prompt**. Reads `system_prompt.md` to assign a role and adds logic to end the conversation upon detecting `完成:` (Done:).
*   **`Agent3.py`**: Has **Local System Command Execution** capabilities. Parses `命令: <command>` from the LLM's reply, executes the command locally via `subprocess`, and returns the result to the LLM for further thinking.
*   **`Agent4.py`**: **CLI Interface Beautification & Refactoring**. Introduces the `rich` library for a high-quality interface and modularizes code logic into functions.
*   **`Agent5.py`**: **Token & Cost Tracking**. Adds the `TokenTracker` to calculate and display token consumption and corresponding estimated costs per round and in total.
*   **`Agent_openrouter.py`**: **Multi-Model Support**. Demonstrates calling other open-source models (e.g., `gemma-4-31b-it:free`) via OpenRouter.

## 🛠️ Environment Dependencies
---
This project uses `uv` for package and virtual environment management, and has built-in `pyproject.toml` and `uv.lock`.
Please ensure that `uv` is installed on your system.

**One-Click Environment & Dependency Installation:**
```bash
uv sync
```
*After running this command, `uv` will automatically read the lock file, create a `.venv` virtual environment for you, and install all required packages.*

## 🚀 Deployment & Execution Guide
---
### 1. Get the Code
Clone or download this project to your local environment:
```bash
git clone <your-repository-url>
cd Very_Simple_Agent
```

### 2. Set Environment Variables (.env)
Create an `.env` file in the root directory of the project and fill in your API Keys. This file is already set in `.gitignore`, so it will not be uploaded to GitHub, ensuring password security.

Add the following content to `.env`:
```env
# OpenAI Key (used by Agent1~5)
OPENAI_API_KEY=sk-your-openai-key-here

# OpenRouter Key (used by Agent_openrouter.py)
OPENROUTER_API_KEY=sk-or-your-openrouter-key-here
```

### 3. Customize System Prompt (Optional)
You can open `system_prompt.md` to freely modify the Agent's role settings and rules.

### 4. Execute the Agent
You can start experiencing it from `Agent5.py`, which is currently the most complete version.
Because the project is configured with `uv`, you can execute it with one click using the following command, and `uv` will automatically ensure it runs in the virtual environment:
```bash
uv run Agents/Agent5.py
```
*(Please make sure to run this command in the project root directory)*

After entering the conversation, you will see a beautiful startup panel and the `>>` prompt.
*   Enter the question you want to ask or the local operation command you want it to perform for you.
*   To exit the conversation, enter `exit`.
