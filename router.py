from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
    APIRouter
)

from ppt_gen import parse_pdf_impl, parse_topic_impl, generate_ppt_impl

app = FastAPI()
pptHandler = APIRouter(prefix="/ppt")
app.include_router(pptHandler)


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
