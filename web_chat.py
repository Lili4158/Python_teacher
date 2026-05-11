import streamlit as st
import requests
import json

# 页面配置
st.set_page_config(page_title="AI聊天助手", layout="wide")

# 初始化聊天
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏
with st.sidebar:
    st.title("⚙️ 设置")
    api_key = st.text_input("输入阿里云百炼 API Key", type="password")
    st.markdown("---")

    # 角色选择
    personality = st.selectbox(
        "选择角色",
        ["专业老师", "程序员助手", "暖心闺蜜", "好兄弟", "男朋友", "女朋友"]
    )

    st.markdown("---")
    if st.button("🗑️ 清空聊天记录"):
        st.session_state.messages = []
        st.rerun()

# 人设提示词
def get_system_prompt(p):
    prompts = {
        "专业老师": "你是耐心专业的老师，清晰解答问题。",
        "程序员助手": "你是资深程序员，擅长代码讲解。",
        "暖心闺蜜": "你是温柔暖心的闺蜜，会倾听安慰。",
        "好兄弟": "你是仗义的好兄弟，重情义，会陪伴。",
        "男朋友": "你是可靠的男朋友，会撑腰、倾听、支持。",
        "女朋友": "你是温柔可爱的女朋友，体贴暖心。"
    }
    return prompts.get(p, "你是贴心AI助手。")

# 聊天界面
st.title(f"🤖 AI助手 - {personality}")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 输入框
prompt = st.chat_input("输入消息...")

if prompt and api_key:
    try:
        # 阿里云百炼的API地址（兼容通义千问）
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 构建请求数据
        system_prompt = get_system_prompt(personality)
        messages = [
            {"role": "system", "content": system_prompt}
        ] + st.session_state.messages + [{"role": "user", "content": prompt}]

        data = {
            "model": "qwen-turbo",  # 通义千问的模型名
            "input": {
                "messages": messages
            },
            "parameters": {
                "result_format": "message"
            }
        }

        # 发送请求
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 检查请求是否成功
        result = response.json()

        # 获取回复
        reply = result["output"]["choices"][0]["message"]["content"]

        # 显示消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"出错：{str(e)}")