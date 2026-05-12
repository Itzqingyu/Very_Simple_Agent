# Very Simple Agent
[English](README.md) | [繁體中文](README.zh-TW.md)

---
這是一個以 Python 實作的輕量化、漸進式 AI Agent 專案。
專案展示了如何從最基礎的 API 呼叫，一步一步進階到擁有精美 CLI 介面、且具備本機命令列操作能力的自主 Agent。

## ✨ 核心功能
---
*   **漸進式學習架構**：從 `Agent1.py` 到 `Agent5.py`，展示了 Agent 功能的迭代過程。
*   **本機系統命令執行**：Agent 能夠解析對話意圖，產生並透過 `subprocess` 執行本機終端機 (bash/cmd) 指令，並能捕捉正確輸出與系統報錯，實現與本機環境的真實互動。
*   **精美的 CLI 介面**：使用 `rich` 套件打造了終端機下的高質感互動介面，包含提示面板、顏色標註與分隔線。
*   **Token 與費用追蹤**：具備紀錄 Token 消耗量與計算 API 使用費用的功能 (`Agent5.py`)。
*   **提示詞外置**：系統提示詞（System Prompt）獨立存放在 `system_prompt.md`，方便隨時調整 Agent 角色設定與行為準則。
*   **多模型支援**：除了支援官方 OpenAI API，也提供 `Agent_openrouter.py` 示範如何串接 OpenRouter 以使用其他開源模型（如 Gemma 等）。

## 🗂️ 專案結構與版本歷史
---
本專案經歷了數次重要的版本迭代（參考 Git Log）：
1. **初始化與基礎串接**：建立基礎目錄、設置 `.gitignore`，完成基本的 OpenAI 與 OpenRouter 串接。
2. **重構系統提示詞**：將原本寫死在程式碼中的 prompt 獨立抽出至 `system_prompt.md`。
3. **優化 CLI 與系統互動機制**：在最新版的腳本中重構了程式結構，加入 `rich` 介面，並且完善了系統指令執行與報錯（`stderr`）捕捉機制。
4. **漸進式功能整合**：拆分為 `Agent1_Basic.py` ~ `Agent5_TokenCount.py`，完整記錄功能的演進。

### 🕵️ Agent 演進分析
*   **`Agent1_Basic.py`**: 最基礎的串接。讀取 `.env` 金鑰，使用 `gpt-4o-mini` 進行一問一答對話。使用 `litellm` 套件 (Agent1 ~ 5)。
*   **`Agent2_SysPrompt.py`**: 加入**系統提示詞**。讀取 `system_prompt.md` 賦予角色設定，加入判斷 `完成:` 結束對話的邏輯。
*   **`Agent3_AgentLoop.py`**: 具備**本機系統命令執行**能力。解析 LLM 回覆中的 `命令: <command>`，透過 `subprocess` 在本機執行指令並回傳結果給 LLM 繼續思考。
*   **`Agent4_FancyCLI.py`**: **CLI 介面美化與重構**。引入 `rich` 套件打造高質感介面，程式邏輯模組化拆分為函式。
*   **`Agent5_TokenCount.py`**: **Token 與費用追蹤**。加入 `TokenTracker`，計算並顯示每輪與總計的 Token 消耗及對應的預估花費。
*   **`Agent_openaiSDK.py`**: **原生 OpenAI SDK 實作**。功能與 Agent 5 類似，但示範如何使用官方 OpenAI SDK 直接呼叫模型，而非透過 `litellm`。
*   **`Agent_openrouter.py`**: **多模型支援**。示範透過 OpenRouter 呼叫其他開源模型 (如 `gemma-4-31b-it:free`)。

## 🛠️ 環境依賴
---
本專案使用 `uv` 進行套件與虛擬環境管理，並已內建 `pyproject.toml` 與 `uv.lock`。
請確保系統已安裝 `uv`。

**一鍵安裝環境與依賴：**
```bash
uv sync
```
*執行此指令後，`uv` 會自動讀取鎖定檔，為您建立 `.venv` 虛擬環境並安裝所有依賴套件。*

## 🚀 部署與執行教學
---
### 1. 取得程式碼
將此專案 Clone 或下載到你的本機環境中：
```bash
git clone <此庫網址>
cd Very_Simple_Agent
```

### 2. 設定環境變數 (.env)
在專案根目錄建立一個 `.env` 檔案，並填入你的 API Key。這份檔案已經被設定在 `.gitignore` 中，因此不會被上傳到 GitHub，可確保密碼安全。

在 `.env` 中加入以下內容：
```env
# OpenAI 金鑰 (Agent1~5 使用)
OPENAI_API_KEY=sk-你的OpenAI金鑰填這裡

# GEMINI 金鑰 (Agent1~5 使用，需自行替換模型)
GEMINI_API_KEY=你的Gemini金鑰填這裡

# OpenRouter 金鑰 (Agent_openrouter.py 使用)
OPENROUTER_API_KEY=sk-or-你的OpenRouter金鑰填這裡
```

### 3. 自訂系統提示詞 (選項)
你可以開啟 `system_prompt.md` 自由修改 Agent 的角色設定與規則。

### 4. 執行 Agent
你可以從 `Agent5_TokenCount.py` 也就是目前功能最完整的版本開始體驗。
因為專案有配置 `uv`，你可以直接透過以下指令一鍵執行，`uv` 會自動確保在虛擬環境中運行：
```bash
uv run Agents/Agent5_TokenCount.py
```
*(請確保在專案根目錄下執行此指令)*

進入對話後，你會看到精美的啟動面板與 `>>` 提示字元。
*   輸入你想問的問題或想請它代勞的本機操作指令。
*   若要離開對話，請輸入 `exit`。
