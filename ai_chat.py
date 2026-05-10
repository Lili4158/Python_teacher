from openai import OpenAI

# 你的API Key
API_KEY = "sk-c91dfb70aa6441e3bce326eb77e76e58"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# ===========================
# 对话历史（AI 能记住你说的话）
# ===========================
messages = [
    {"role": "system", "content": "你是一个友好的AI助手，会记住对话内容"}
]


# ===========================
# 自动保存聊天到文件
# ===========================
def save_chat(user_text, ai_reply):
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"你：{user_text}\n")
        f.write(f"AI：{ai_reply}\n")
        f.write("------------------------------\n")


# ===========================
# 与AI对话的函数
# ===========================
def chat_with_ai(user_input):
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=messages
    )

    ai_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_reply})

    # 自动保存
    save_chat(user_input, ai_reply)

    return ai_reply


# ===========================
# 启动程序
# ===========================
print("✅ AI机器人已启动！带记忆 + 自动保存聊天记录")
print("输入 exit 退出\n")

while True:
    user_text = input("你：")

    if user_text.lower() == "exit":
        print("👋 再见！聊天记录已保存到 chat_history.txt")
        break

    ai_reply = chat_with_ai(user_text)
    print(f"AI：{ai_reply}\n")