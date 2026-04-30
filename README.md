# Very Simple Agent
---
這是一個以 Python 實作的輕量化、漸進式 AI Agent 專案。
專案展示了如何從最基礎的 API 呼叫，一步一步進階到擁有精美 CLI 介面、且具備本機命令列操作能力的自主 Agent。

## ✨ 核心功能
---
*   **漸進式學習架構**：從 `Agent1.py` 到 `Agent4.py`，展示了 Agent 功能的迭代過程。
*   **本機系統命令執行**：Agent 能夠解析對話意圖，產生並透過 `subprocess` 執行本機終端機 (bash/cmd) 指令，並能捕捉正確輸出與系統報錯，實現與本機環境的真實互動。
*   **精美的 CLI 介面**：使用 `rich` 套件打造了終端機下的高質感互動介面，包含提示面板、顏色標註與分隔線。
*   **提示詞外置**：系統提示詞（System Prompt）獨立存放在 `system_prompt.md`，方便隨時調整 Agent 角色設定與行為準則。
*   **多模型支援**：除了支援官方 OpenAI API，也提供 `Agent_openrouter.py` 示範如何串接 OpenRouter 以使用其他開源模型（如 Gemma 等）。

## 🗂️ 專案結構與版本歷史
---
本專案經歷了數次重要的版本迭代（參考 Git Log）：
1. **初始化與基礎串接**：建立基礎目錄、設置 `.gitignore`，完成基本的 OpenAI 與 OpenRouter 串接。
2. **重構系統提示詞**：將原本寫死在程式碼中的 prompt 獨立抽出至 `system_prompt.md`。
3. **優化 CLI 與系統互動機制**：在最新版的腳本中重構了程式結構，加入 `rich` 介面，並且完善了系統指令執行與報錯（`stderr`）捕捉機制。
4. **漸進式功能整合**：拆分為 `Agent1.py` ~ `Agent4.py`，完整記錄功能的演進。

## 🛠️ 環境依賴
---
請確保你的環境安裝了 Python 3，並安裝以下第三方套件：
*   `openai` - 用於呼叫 OpenAI 官方或相容規格之 API
*   `python-dotenv` - 用於安全地讀取 `.env` 中的環境變數
*   `rich` - 用於繪製終端機內的精美 UI 與顏色

**快速安裝指令：**
```bash
pip install openai python-dotenv rich
```

## 🚀 部署與執行教學
---
### 1. 取得程式碼
將此專案 Clone 或下載到你的本機環境中：
```bash
git clone <你的儲存庫網址>
cd Very_Simple_Agent
```

### 2. 設定環境變數 (.env)
在專案根目錄建立一個 `.env` 檔案，並填入你的 API Key。這份檔案已經被設定在 `.gitignore` 中，因此不會被上傳到 GitHub，可確保密碼安全。

在 `.env` 中加入以下內容：
```env
# OpenAI 金鑰 (Agent1~4 使用)
OPENAI_API_KEY=sk-你的OpenAI金鑰填這裡

# OpenRouter 金鑰 (Agent_openrouter.py 使用)
OPENROUTER_API_KEY=sk-or-你的OpenRouter金鑰填這裡
```

### 3. 自訂系統提示詞 (選項)
你可以開啟 `system_prompt.md` 自由修改 Agent 的角色設定與規則。

### 4. 執行 Agent
你可以從 `Agent4.py` 也就是功能最完整的版本開始體驗。
在終端機輸入：
```bash
python Agent4.py
```

進入對話後，你會看到精美的啟動面板與 `>>` 提示字元。
*   輸入你想問的問題或想請它代勞的本機操作指令。
*   若要離開對話，請輸入 `exit`。
