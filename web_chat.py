import streamlit as st
from openai import OpenAI

# 页面配置
st.set_page_config(page_title="AI聊天助手", layout="wide")

# 初始化聊天
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏
with st.sidebar:
    st.title("⚙️ 设置")
    api_key = st.text_input("输入 API Key", type="password")
    st.markdown("---")

    # 所有人设都在这里
    personality = st.selectbox(
        "选择角色",
        ["专业老师", "程序员助手", "暖心闺蜜", "好兄弟", "男朋友", "女朋友"]
    )

    st.markdown("---")
    if st.button("🗑️ 清空聊天"):
        st.session_state.messages = []
        st.rerun()

# 人设提示词
def get_system_prompt(p):
    if p == "专业老师":
        return "你是耐心专业的老师，清晰解答问题。"
    elif p == "程序员助手":
        return "你是资深程序员，擅长代码讲解。"
    elif p == "暖心闺蜜":
        return "你是温柔暖心的闺蜜，会倾听安慰。"
    elif p == "好兄弟":
        return "你是仗义的好兄弟，重情义，会陪伴。"
    elif p == "男朋友":
        return "你是可靠的男朋友，会撑腰、倾听、支持。"
    elif p == "女朋友":
        return "你是温柔可爱的女朋友，体贴暖心。"
    return "你是贴心AI助手。"

# 聊天界面
st.title(f"🤖 AI助手 - {personality}")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 输入框
prompt = st.chat_input("输入消息...")

if prompt and api_key:
    try:
        # 最新稳定代理（今天可用）
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.oaiproxy.vip/v1"
        )

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        messages = [
            {"role": "system", "content": get_system_prompt(personality)}
        ] + st.session_state.messages

        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = res.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"出错：{str(e)}")