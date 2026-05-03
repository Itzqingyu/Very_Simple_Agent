from litellm import completion, completion_cost
import os
import subprocess
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

# 初始化 Console
console = Console()

class TokenTracker:
    """追蹤整個 session 的 token 使用量與費用"""

    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost_usd = 0.0
        # 單輪 agent 循環的暫存計數
        self.loop_input_tokens = 0
        self.loop_output_tokens = 0
        self.loop_cost_usd = 0.0

    def update(self, response):
        """從 response 累加 token 並透過 litellm 計算費用"""
        usage = response.usage
        cost = completion_cost(completion_response=response)
        self.total_input_tokens  += usage.prompt_tokens
        self.total_output_tokens += usage.completion_tokens
        self.total_cost_usd      += cost
        self.loop_input_tokens   += usage.prompt_tokens
        self.loop_output_tokens  += usage.completion_tokens
        self.loop_cost_usd       += cost

    def reset_loop(self):
        """重置單輪計數（每輪 agent 循環開始時呼叫）"""
        self.loop_input_tokens = 0
        self.loop_output_tokens = 0
        self.loop_cost_usd = 0.0

    @property
    def loop_tokens(self):
        return self.loop_input_tokens + self.loop_output_tokens

    @property
    def loop_cost(self):
        return self.loop_cost_usd

    @property
    def total_tokens(self):
        return self.total_input_tokens + self.total_output_tokens

    @property
    def total_cost(self):
        return self.total_cost_usd

def init_agent():
    """初始化環境變數與系統提示詞"""
    load_dotenv()
    
    with open("system_prompt.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()
        
    messages = [{"role": "system", "content": system_prompt}]
    return messages

def print_welcome_panel():
    """顯示頂部的狀態資訊面板"""
    info_text = (
        "模型  gemini/gemini-2.5-flash\n"
        "狀態  準備就緒"
    )
    console.print(Panel(info_text, title="✦ Agent 小助手 ✦", border_style="dim", expand=False))

def call_llm(messages):
    """呼叫大語言模型並回傳結果"""
    response = completion(
        model="gemini/gemini-2.5-flash", 
        messages=messages
    )
    return response

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

def print_loop_stats(tracker):
    """顯示單輪 agent 循環的 token 用量"""
    stats = (
        f"\n本輪消耗 Tokens: {tracker.loop_tokens:,} "
        f"(輸入 {tracker.loop_input_tokens:,} + 輸出 {tracker.loop_output_tokens:,})\n"
        f"預期花費: $ {tracker.loop_cost:.6f} USD"
    )
    console.print(f"[dim]{stats}[/dim]")

def print_summary_panel(tracker):
    """顯示本次對話的 token 使用量與費用"""
    summary = (
        f"輸入 tokens   {tracker.total_input_tokens:,}\n"
        f"輸出 tokens   {tracker.total_output_tokens:,}\n"
        f"總計 tokens   {tracker.total_tokens:,}\n"
        f"預估花費      ${tracker.total_cost:.6f} USD"
    )
    console.print()
    console.print(Panel(summary, title="📊 Token 使用統計", border_style="green", expand=False))

# ---------- main ----------

def main():
    messages = init_agent()
    tracker = TokenTracker()
    print_welcome_panel()

    # 主對話循環
    while True:
        console.print()
        user_input = console.input("[bold white]>> [/bold white]")
        
        if user_input.lower() == "exit":
            print_summary_panel(tracker)
            break

        messages.append({"role": "user", "content": user_input})

        console.print("\n[dim]─────────────────────────────────────────────────────────────────────────────────────────────────[/dim]")
        console.print(f"[[white]Agent -> AI[/white]] {user_input} (+ 系統提示詞)")

        tracker.reset_loop()

        # Agent 內部思考/執行循環
        while True:
            response = call_llm(messages)
            reply = response.choices[0].message.content
            tracker.update(response)
            messages.append({"role": "assistant", "content": reply})

            # 印出大模型的回覆
            console.print(f"[[white]AI -> Agent[/white]] {reply}")

            if reply.strip().startswith("完成:"):
                print_loop_stats(tracker)
                break

            # 若是 "命令: " 開頭，執行命令並將執行結果加入對話歷史
            command_output = execute_system_command(reply)
            messages.append({"role": "user", "content": command_output})

if __name__ == "__main__":
    main()