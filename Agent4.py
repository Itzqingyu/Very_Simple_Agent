from openai import OpenAI
import os
import subprocess
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

# 初始化 Console
console = Console()

def init_agent():
    """初始化環境變數、OpenAI 客戶端與系統提示詞"""
    load_dotenv()
    
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    with open("system_prompt.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()
        
    messages = [{"role": "system", "content": system_prompt}]
    return client, messages

def print_welcome_panel():
    """顯示頂部的狀態資訊面板"""
    info_text = (
        "模型  gpt-4o-mini\n"
        "狀態  準備就緒 (先略過 token 計算)"
    )
    console.print(Panel(info_text, title="✦ Agent 小助手 ✦", border_style="dim", expand=False))

def call_llm(client, messages):
    """呼叫大語言模型並回傳結果"""
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=messages
    )
    return response.choices[0].message.content

def execute_system_command(reply):
    """解析 LLM 回覆中的命令並在系統執行，回傳執行結果字串"""
    try:
        command = reply.strip().split("命令:")[1].strip()
        
        # 使用 subprocess 執行命令並捕捉 stdout 與 stderr
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # 合併正常輸出與錯誤輸出
        command_result = process.stdout.strip()
        if process.stderr.strip():
            command_result = (command_result + "\n" + process.stderr.strip()).strip()
        
        command_output = f"執行命令結果 (無則為無報錯): {command_result}"
        console.print(f"[[dim]BASH[/dim]] {command_result}")
        console.print(f"[[dim]Agent -> AI[/dim]] {command_output}")
        
        return command_output
    except IndexError:
        error_msg = "系統回傳: 無法解析命令，請確認格式是否包含 '命令:'"
        console.print(f"[[red]系統 -> Agent[/red]] {error_msg}")
        return error_msg

def main():
    client, messages = init_agent()
    print_welcome_panel()

    # 主對話循環
    while True:
        console.print()
        user_input = console.input("[bold white]>> [/bold white]")
        
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        console.print("\n[dim]─────────────────────────────────────────────────────────────────────────────────────────────────[/dim]")
        console.print(f"[[white]Agent -> AI[/white]] {user_input} (+ 系統提示詞)")

        # Agent 內部思考/執行循環
        while True:
            reply = call_llm(client, messages)
            messages.append({"role": "assistant", "content": reply})

            # 印出大模型的回覆
            console.print(f"[[white]AI -> Agent[/white]] {reply}")

            if reply.strip().startswith("完成:"):
                break

            # 若是 "命令: " 開頭，執行命令並將執行結果加入對話歷史
            command_output = execute_system_command(reply)
            messages.append({"role": "user", "content": command_output})

if __name__ == "__main__":
    main()