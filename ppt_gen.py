import hashlib
import os
import uuid
from datetime import datetime

from fastapi import (
    File,
    UploadFile
)
from fastapi.logger import logger
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

import config
from prompts import gen_ppt_md

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


async def download_pdf_impl(
        topic: str,
        style: str,
        pptx_file: UploadFile = File(...)
):
    task_id = datetime.now().strftime("20%y-%m-%d") + "/" + str(uuid.uuid4())
    logger.info(f"task created: {task_id}")
    os.makedirs(os.path.join(config.RUNS_DIR, task_id))
    task = {
        "topic": topic,
        "pptx": "default_template"
    }
    if pptx_file is not None:
        pptx_blob = await pptx_file.read()
        pptx_md5 = hashlib.md5(pptx_blob).hexdigest()
        task["pptx"] = pptx_md5
        pptx_dir = os.path.join(config.RUNS_DIR, "pptx", pptx_md5)
        if not os.path.exists(pptx_dir):
            os.makedirs(pptx_dir, exist_ok=True)
            data = ask_query("人工智能", "关于大模型")
            print(data)


def ask_query(schema, style):
    prompt = gen_ppt_md(schema)
    messages = [
        (
            "system",
            prompt,
        ),
        ("human", style),
    ]
    response = llm.invoke(messages)

    return response.content


if __name__ == '__main__':
    data = ask_query("人工智能", "关于大模型")
    print(data)
