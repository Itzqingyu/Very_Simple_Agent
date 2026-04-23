from openai import OpenAI
import os
from dotenv import load_dotenv

# 讀取 .env 檔案中的隱藏變數
load_dotenv()

# 1. 初始化設定 (告訴 SDK 用 OpenRouter 的通道)
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"), # 從環境變數中讀取金鑰
)

# 初始化 AI
# messages = [{"role": "system", "content": """你的目標是完成用戶指定的任務，你只能以以下其中一種格式，且語言為繁體中文回答，沒有例外：
# 1. 若你認為需要執行指令，輸出「命令: XXX」，XXX為你認為需要執行的指令，且不輸出其他文字。
# 2. 若你認為不用執行指令了，輸出「完成: XXX」，XXX為此次對話你的總結。"""}]
messages = []

while True:
  user_input = input("【你】")
  if user_input == "exit":
    break


  messages.append({"role": "user", "content": user_input})

  # 2. 呼叫大模型
  response = client.chat.completions.create(
    model="google/gemma-4-26b-a4b-it:free", 
    messages=messages
  )
  print("大模型呼叫成功")
  
  reply = response.choices[0].message.content
  messages.append({"role": "assistant", "content": reply})

  # 3. 印出大模型的回覆
  print(f"【AI】{reply}")
  # print(f"所有歷程對話: {messages}")