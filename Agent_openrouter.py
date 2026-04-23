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
with open("system_prompt.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()

messages = [{"role": "system", "content": system_prompt}]

while True:
  user_input = input("【你】")
  if user_input == "exit":
    break


  messages.append({"role": "user", "content": user_input})

  # 2. 呼叫大模型
  response = client.chat.completions.create(
    model="inclusionai/ling-2.6-flash:free", 
    messages=messages
  )
  print("大模型呼叫成功")
  
  reply = response.choices[0].message.content
  messages.append({"role": "assistant", "content": reply})

  # 3. 印出大模型的回覆
  print(f"【AI】{reply}")
  # print(f"所有歷程對話: {messages}")