from openai import OpenAI

API_KEY = "sk-c91dfb70aa6441e3bce326eb77e76e58"
client = OpenAI(api_key=API_KEY, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")


def process_text(text, task="帮我总结成1句话"):
    """让AI处理单条文本，task可以改成翻译、提取关键词等"""
    prompt = f"{task}：{text}"
    response = client.chat.completions.create(
        model="qwen-turbo-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def batch_process():
    # 1. 读取input.txt里的所有文本
    with open("input.txt", "r", encoding="utf-8") as f:
        texts = [line.strip() for line in f if line.strip()]  # 跳过空行

    print(f"📄 共读取到 {len(texts)} 条文本，开始处理...")

    # 2. 循环处理每一条文本
    results = []
    for i, text in enumerate(texts, 1):
        print(f"正在处理第 {i}/{len(texts)} 条...")
        result = process_text(text, task="帮我总结成1句话")  # 这里可以改任务
        results.append((text, result))

    # 3. 把结果保存到output.txt
    with open("output.txt", "w", encoding="utf-8") as f:
        for text, result in results:
            f.write(f"原文：{text}\n")
            f.write(f"结果：{result}\n")
            f.write("=" * 30 + "\n")

    print("✅ 处理完成！结果已保存到 output.txt")


if __name__ == "__main__":
    # 先创建input.txt，输入要处理的内容
    print("请在当前文件夹创建 input.txt，每行写一条要处理的文本，然后按回车继续...")
    input()
    batch_process()