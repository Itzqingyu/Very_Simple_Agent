from openai import OpenAI
import os
from dotenv import load_dotenv

# 初始化 (讀取 KEY、指定 client、載入 system_prompt)

load_dotenv()

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
)

with open("system_prompt.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()

messages = [{"role": "system", "content": system_prompt}]

# 對話循環
while True:
  user_input = input("【你】")
  if user_input == "exit":
    break

  messages.append({"role": "user", "content": user_input})

  print("----- Agent 循環開始 -----")
  while True:
    # 呼叫大模型
    response = client.chat.completions.create(
      model="gpt-4o-mini", 
      messages=messages
    )
    
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    # 印出大模型的回覆
    print(f"【AI】{reply}")

    if reply.strip().startswith("完成:"):
      print("----- Agent 循環結束 -----")
      break

    command = reply.strip().split("命令:")[1].strip()
    command_result = os.popen(command).read()

    command_output = f"已執行 LLM 後的系統回傳結果 (無則為無報錯) {command_result}"
    print(f"【Agent】{command_output}")
    messages.append({"role": "user", "content": command_output})