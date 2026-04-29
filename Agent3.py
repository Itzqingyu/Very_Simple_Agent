from openai import OpenAI
import os
import subprocess
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
  user_input = input("\n>> ")
  if user_input.lower() == "exit":
    break

  messages.append({"role": "user", "content": user_input})

  print("-------------------- Agent 循環開始 --------------------")
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
      print("-------------------- Agent 循環結束 --------------------\n")
      break

    command = reply.strip().split("命令:")[1].strip()
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    command_result = process.stdout.strip()
    if process.stderr.strip():
      command_result = (command_result + "\n" + process.stderr.strip()).strip()

    command_output = f"執行命令結果 (無則為無報錯): {command_result}"
    print(f"【BASH】{command_result}")
    print(f"【Agent】{command_output}")
    messages.append({"role": "user", "content": command_output})