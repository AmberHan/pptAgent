import os
import subprocess


def generate_png(ppt_path: str, output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        # 1、把ppt转化为pdf LibreOffice
        subprocess.run([
            "soffice",
            '--headless',
            '--convert-to', 'png',
            '--outdir', output_dir,
            ppt_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        pass


# 查看目录下所有地址
def list_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            generate_png(os.path.abspath(os.path.join(root, file)), "../first_pages")
            # print(os.path.abspath(os.path.join(root, file)))


list_files_in_directory("../模板2")
