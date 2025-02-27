from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
    APIRouter
)

from ppt_gen import download_pdf_impl

app = FastAPI()
pptHandler = APIRouter(prefix="/ppt")
app.include_router(pptHandler)


@pptHandler.post("/api/upload")
async def create_ppt_task(
        pptx_file: UploadFile = File(...),
        topic: str = Form(None),
        style: str = Form(None)
):
    return download_pdf_impl(topic, style, pptx_file)


@pptHandler.post("/api/topic")
async def create_ppt_task(
        topic: str = Form(None),
        style: str = Form(None)
):
    return download_pdf_impl(topic, style)
