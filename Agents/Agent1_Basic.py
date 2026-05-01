from litellm import completion
from dotenv import load_dotenv

# 讀取 .env 檔案中的隱藏變數
load_dotenv()

messages = []

# 對話輸入循環
while True:
  user_input = input("【你】")
  if user_input == "exit":
    break

  messages.append({"role": "user", "content": user_input})

  # 呼叫大模型
  response = completion(
    model="gpt-4o-mini", 
    messages=messages
  )

  reply = response.choices[0].message.content
  messages.append({"role": "assistant", "content": reply})

  # 印出大模型的回覆
  print(f"【AI】{reply}")