import streamlit as st
from openai import OpenAI
import datetime

# ---------------------- 页面设置 ----------------------
st.set_page_config(page_title="AI智能聊天助手", layout="wide")

# ---------------------- 侧边栏 ----------------------
with st.sidebar:
    st.title("⚙️ 设置面板")

    # 读取API Key（优先读Streamlit密钥，再读用户输入）
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        api_key = st.text_input("输入 OpenAI API Key", type="password")

    st.markdown("---")

    # 所有新人设（已完整包含）
    personality = st.selectbox(
        "选择AI角色",
        ["专业老师", "程序员助手", "暖心闺蜜", "好兄弟", "男朋友", "女朋友"]
    )

    st.markdown("---")
    if st.button("🗑️ 清空所有聊天记录"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    if st.button("📥 导出聊天记录"):
        if "messages" in st.session_state and len(st.session_state.messages) > 0:
            content = ""
            for msg in st.session_state.messages:
                content += f"[{msg['role']}]\n{msg['content']}\n\n"
            st.download_button(
                label="点击保存聊天记录",
                data=content,
                file_name=f"聊天记录_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )


# ---------------------- 人设系统 ----------------------
def get_system_prompt(personality):
    if personality == "专业老师":
        return "你是一位耐心、专业的老师，回答清晰、简洁、有逻辑，擅长讲解知识。"
    elif personality == "程序员助手":
        return "你是资深程序员，擅长代码解释、bug修复、编程教学。"
    elif personality == "暖心闺蜜":
        return "你是温柔暖心的闺蜜，会倾听、安慰、陪伴，语气亲切温暖。"
    elif personality == "好兄弟":
        return "你是为人仗义、情如手足的兄弟，重情义、体谅人，擅长倾听和安慰。"
    elif personality == "男朋友":
        return "你是可靠的男朋友，是靠山、精神支柱，会倾听、撑腰，用行动表达爱意，三观正。"
    elif personality == "女朋友":
        return "你是温柔可爱的女朋友，体贴、暖心、会撒娇、会陪伴。"
    else:
        return "你是一个贴心的AI助手，会耐心解答你的所有问题。"


# ---------------------- 初始化聊天 ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------- 标题 ----------------------
st.title("🤖 AI智能聊天助手")
st.caption(f"当前角色：{personality}")

# ---------------------- 展示聊天记录 ----------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------- 输入框 ----------------------
prompt = st.chat_input("请输入你的问题...")

if prompt:
    if not api_key:
        st.warning("⚠️ 请先在侧边栏输入 API Key 才能聊天！")
    else:
        # 关键修复：加上国内API代理地址！！！
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.aiproxy.io/v1"  # 国内平台通用代理地址
        )

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        system_prompt = get_system_prompt(personality)
        messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})