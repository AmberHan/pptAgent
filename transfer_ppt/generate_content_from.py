import sys

import PyPDF2
from docx import Document as DocxDocument
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

sys.path.append("../")
import config


# 3. 加载文件内容
def load_file_content(file_path):
    """
    从文件中加载文本内容
    """
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    elif file_path.endswith(".docx"):
        doc = DocxDocument(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".pdf"):
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            return text
    else:
        raise ValueError("不支持的文件格式")


# 4. 使用模型解析内容
def parse_content_with_model(text, llm):
    """
    使用 MoonshotChat 解析文本内容，提取标题和段落
    """
    # 构造提示词
    prompt = f"""
    以下是一段文档内容：
    {text}

    请解析该文档，提取以下信息：
    1. 标题分级
    2. 段落内容

    返回格式：
    以markdown格式输出包括标题和段落
    """

    # 调用模型
    response = llm.predict(prompt)
    return response


# 5. 主函数
def get_content_value(path: str):
    if config.LOCAL:
        llm = ChatOllama(
            model=config.MODEL,  # "Qwen2.5-72B-Instruct",
            temperature=0.7,
            base_url=config.BASE_URL  # "http://127.0.0.1:11434",
        )
    else:
        llm = ChatOpenAI(
            model=config.MODEL,
            temperature=0.7,
            api_key=config.API_KEY,
            base_url=config.BASE_URL
        )

    file_path = path
    text = load_file_content(file_path)
    result = parse_content_with_model(text, llm)
    print("解析结果：")
    md = result.replace("```", "").replace("markdown", "")
    print(md)
    return md
