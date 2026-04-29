from openai import OpenAI
import os
from dotenv import load_dotenv

# 讀取 .env 檔案中的隱藏變數
load_dotenv()

# 1. 初始化設定
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
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

  while True:
    # 2. 呼叫大模型
    response = client.chat.completions.create(
      model="gpt-4o-mini", 
      messages=messages
    )
    
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    # 3. 印出大模型的回覆
    print(f"【AI】{reply}")
    # print(f"所有歷程對話: {messages}")

    # 4. 判斷是否需要繼續
    if reply.startswith("完成:"):
      break