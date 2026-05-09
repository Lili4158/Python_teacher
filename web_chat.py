import streamlit as st
from openai import OpenAI

# 你的API Key
# 从Streamlit的安全密钥中读取API Key
API_KEY = st.secrets["API_KEY"]
client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 初始化对话历史（带完整的system提示词）
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system",
         "content": "你是一位耐心的Python编程老师，会用通俗易懂的方式教用户Python知识，解答编程问题，帮用户写代码并解释思路。"}
    ]

# 页面标题
st.title("杨爽专属Ai")

# 侧边栏：清空对话历史（保留system提示词）
with st.sidebar:
    st.title("设置")
    if st.button("清空对话历史"):
        st.session_state.messages = [
            {"role": "system",
             "content": "你是一位耐心的Python编程老师，会用通俗易懂的方式教用户Python知识，解答编程问题，帮用户写代码并解释思路。"}
        ]
        st.rerun()

# 渲染历史对话
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 用户输入框
if prompt := st.chat_input("你想说点什么？"):
    # 把用户输入加入历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 调用AI并显示回复
    with st.chat_message("assistant"):
        with st.spinner("AI正在思考..."):
            response = client.chat.completions.create(
                model="qwen-turbo-latest",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.write(reply)

    # 把AI回复加入历史
    st.session_state.messages.append({"role": "assistant", "content": reply})