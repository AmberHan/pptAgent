import os
import uuid
from datetime import datetime

import json5
from fastapi import (
    File,
    UploadFile
)
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

import config
from ppt import generate
from prompts import gen_ppt_md, gen_md_json
from test_data import markdown_content

if config.LOCAL:
    llm = ChatOllama(
        model=config.MODEL,  # "Qwen2.5-72B-Instruct",
        temperature=0.7,
        base_url=config.BASEURL  # "http://127.0.0.1:11434",
    )
else:
    llm = ChatOpenAI(
        model=config.MODEL,
        temperature=0.7,
        api_key=config.APIKEY,
        base_url=config.BASEURL
    )


def ask_query(prompt, style):
    messages = [
        (
            "system",
            prompt,
        ),
        ("human", style),
    ]
    response = llm.invoke(messages)
    data = response.content
    print(data)
    return data


async def parse_pdf_impl(
        topic: str,
        style: str,
        pdf_file: UploadFile = File(...)
):
    task_id = datetime.now().strftime("20%y-%m-%d") + "/" + str(uuid.uuid4())
    run_dir = os.path.join(config.RUNS_DIR, task_id)
    os.makedirs(run_dir, exist_ok=True)
    pdf_save_path = os.path.join(run_dir, pdf_file.filename)
    with open(pdf_save_path, 'wb') as f:
        pdf_blob = await pdf_file.read()
        f.write(pdf_blob)
    # todo 解析PDF或文档，文档保存在pdf_save_path，返回md文件
    prompt = gen_ppt_md(topic)
    return ask_query(prompt, style)


def parse_topic_impl(
        topic: str,
        style: str,
):
    return ask_query(gen_ppt_md(topic), style)


def generate_ppt_impl(
        md: str,
        ppt_path: str
):
    prompt = gen_md_json()
    json_content = ask_query(prompt, md)
    generate(ppt_path, json5.loads(json_content))


if __name__ == '__main__':
    # prompt = gen_ppt_md("人工智能")
    # md = ask_query(prompt, "关于大模型")
    md = markdown_content
    parse_md_impl(md, "./ppt_templates/test.pptx")
