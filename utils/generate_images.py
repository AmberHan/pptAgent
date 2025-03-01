import os
import shutil
import subprocess
from datetime import datetime

import pdfplumber

from config import SERVER_IP


def convert_ppt_to_images():
    file_name = 'final.pptx'
    ppt_file = os.path.abspath("./final.pptx")
    output_dir = "output_images"

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  # 删除整个目录
    os.makedirs(output_dir)

    try:
        subprocess.run([
            "soffice",
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            ppt_file
        ], check=True)
    except subprocess.CalledProcessError as e:
        pass

    pdf_file = os.path.join(output_dir, file_name)
    image_list = []

    try:
        with pdfplumber.open(pdf_file.split(".")[0] + ".pdf") as pdf:
            for i, page in enumerate(pdf.pages):  # Convert the first two pages
                im = page.to_image(resolution=150)
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                image_path = os.path.join(output_dir, f"page-{i + 1}_{current_time}.png")
                im.save(image_path)
                image_list.append(f"http://{SERVER_IP}/static/output_images/{os.path.basename(image_path)}")
                print(image_list)
                print(f'---- Split line, Page {i + 1} ----')

    except Exception as e:
        pass

    return image_list
