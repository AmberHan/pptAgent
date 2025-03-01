import os

from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
    APIRouter
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from config import SERVER_IP
from ppt_llm import parse_pdf_impl, parse_topic_impl, generate_ppt_impl, ask_query
from prompts import gen_ppt_md
from transfer_ppt.generate_content_from import get_content_value
from utils.generate_images import convert_ppt_to_images

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
pptHandler = APIRouter(prefix="/ppt")


class RequestData(BaseModel):
    file: str
    content: str


app.mount("/static", StaticFiles(directory="./"), name="static")

file_name_use = ""


# 根据上传文件，返回md文件
@pptHandler.post("/api/upload")
async def pdf_ppt_task(
        pdf_file: UploadFile = File(...),
        topic: str = Form(None),
        style: str = Form(None)
):
    return parse_pdf_impl(topic, style, pdf_file)


# 根据topic，生成md格式文档，并返回txt
@pptHandler.post("/api/topic")
async def topic_ppt_task(
        topic: str = Form(None),
        style: str = Form(None)
):
    return parse_topic_impl(topic, style)


# 根据md文件生成ppt，ppt_path表示模板路径
@pptHandler.post("/api/generatePPT")
async def generate_ppt_task(
        md: str = Form(None),
        ppt_path: str = Form(None)
):
    return generate_ppt_impl(md, ppt_path)


# ==========================================================
# 获取文稿内容
@pptHandler.get("/api/get_content")
def get_content(name: str, count: str):
    try:
        if name != "1":
            prompt = gen_ppt_md(name)
            md = ask_query(prompt, "")
            return JSONResponse(content={"content": md})
        global file_name_use
        file_name = get_content_value(file_name_use)
        reutrn_content = gen_ppt_md(file_name)
        md = ask_query(reutrn_content, "")
        return JSONResponse(content={"content": md})

    except Exception as e:
        # 捕获异常并返回错误信息
        raise JSONResponse(content={"error": str(e)}, status_code=400)


# 获取模板展示
@pptHandler.post("/api/ppt_first_template")
def convert_ppt_first_template():
    image_list = []
    for root, dirs, files in os.walk("first_pages"):
        for file in files:
            print(file)
            image_list.append(f"http://{SERVER_IP}/static/first_pages/{os.path.basename(file)}")
    return JSONResponse(content={"images": image_list})


# 生成ppt最终内容图片
@pptHandler.post("/api/ppt_final_content")
def convert_ppt_first_template(data: RequestData):
    # try:
    generate_ppt_impl(data.content, os.path.abspath("./模板2/" + data.file.split("/")[-1]))
    image_list = convert_ppt_to_images()
    return JSONResponse(content={"images": image_list})
    # except Exception as e:
    #     return JSONResponse(content={"error": str(e)}, status_code=400)


# 上传
@pptHandler.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(f"uploaded_{file.filename}", "wb") as f:
            f.write(contents)
        global file_name_use
        file_name_use = f"uploaded_{file.filename}"
        return JSONResponse(content={"filename": file.filename, "status": "success"})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


app.include_router(pptHandler)
