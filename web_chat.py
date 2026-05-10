import streamlit as st
from openai import OpenAI

# 页面配置（固定，不要动）
st.set_page_config(
    page_title="杨爽AI助手",
    layout="wide"
)

# 阿里云千问配置
API_KEY ="sk-c91dfb70aa6441e3bce326eb77e76e58"
client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个乐于助人的AI助手，会用清晰、友好的方式回答用户的问题。"}
    ]

# 页面标题
st.title("🤖 杨爽AI助手")

# 侧边栏清空功能
with st.sidebar:
    st.subheader("功能区")
    if st.button("🗑️ 清空对话记录"):
        st.session_state.messages = [
            {"role": "system", "content": "你是一个乐于助人的AI助手，会用清晰、友好的方式回答用户的问题。"}
        ]
        st.rerun()

# ---------------------- 核心渲染部分（和当前聊天界面逻辑完全一致） ----------------------
# 1. 先渲染所有历史消息（用户+AI）
for message in st.session_state.messages:
    # 跳过系统提示词，不显示在界面上
    if message["role"] == "system":
        continue

    # 用户消息：右边，蓝色气泡+用户头像
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(
                f"""
                <div style="
                    background-color: #e3f2fd;
                    padding: 12px 16px;
                    border-radius: 18px;
                    text-align: right;
                    max-width: 80%;
                    display: inline-block;
                    margin-left: auto;
                    color: black;
                ">
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    # AI消息：左边，灰色气泡+机器人头像
    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(
                f"""
                <div style="
                    background-color: #f5f5f5;
                    padding: 12px 16px;
                    border-radius: 18px;
                    text-align: left;
                    max-width: 80%;
                    display: inline-block;
                    margin-right: auto;
                    color: black;
                ">
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------------------- 用户输入部分（绝对不会吞消息的逻辑） ----------------------
if prompt := st.chat_input("你想说点什么？"):
    # 步骤1：先把用户消息加入历史（必须放第一行！）
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 步骤2：立刻渲染用户消息（避免第一条消息被吞）
    with st.chat_message("user", avatar="👤"):
        st.markdown(
            f"""
            <div style="
                background-color: #e3f2fd;
                padding: 12px 16px;
                border-radius: 18px;
                text-align: right;
                max-width: 80%;
                display: inline-block;
                margin-left: auto;
                color: black;
            ">
                {prompt}
            </div>
            """,
            unsafe_allow_html=True
        )

    # 步骤3：调用AI并显示回复
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("AI正在思考..."):
            completion = client.chat.completions.create(
                model="qwen-turbo-latest",
                messages=st.session_state.messages
            )
            reply = completion.choices[0].message.content
            st.markdown(
                f"""
                <div style="
                    background-color: #f5f5f5;
                    padding: 12px 16px;
                    border-radius: 18px;
                    text-align: left;
                    max-width: 80%;
                    display: inline-block;
                    margin-right: auto;
                    color: black;
                ">
                    {reply}
                </div>
                """,
                unsafe_allow_html=True
            )

    # 步骤4：把AI回复加入历史
    st.session_state.messages.append({"role": "assistant", "content": reply})