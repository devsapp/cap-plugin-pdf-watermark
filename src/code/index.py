# coding=utf-8
import sys
import json
import os
import requests
import oss2
import uuid
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics, ttfonts

# OSS 配置
OSS_SECURITY_TOKEN = os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")
OSS_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
OSS_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
OSS_ENDPOINT = os.getenv("OSS_ENDPOINT")
OSS_BUCKET = os.getenv("OSS_BUCKET")

pdfmetrics.registerFont(
    ttfonts.TTFont(
        "zenhei", os.path.join("/usr/share/fonts/truetype/wqy", "wqy-zenhei.ttc")
    )
)
pdfmetrics.registerFont(
    ttfonts.TTFont(
        "microhei", os.path.join("/usr/share/fonts/truetype/wqy", "wqy-microhei.ttc")
    )
)


def add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    print(pdf_file_in, pdf_file_mark, pdf_file_out)
    pdf_output = PdfWriter()
    with open(pdf_file_in, "rb") as input_stream:
        pdf_input = PdfReader(input_stream, strict=False)

        # pageNum = pdf_input.getNumPages()
        pageNum = len(pdf_input.pages)
        pdf_watermark = PdfReader(open(pdf_file_mark, "rb"), strict=False)

        for i in range(pageNum):
            page = pdf_input.pages[i]
            page.merge_page(pdf_watermark.pages[0])
            page.compress_content_streams()
            pdf_output.add_page(page)

        with open(pdf_file_out, "wb") as f:
            pdf_output.write(f)


def _create_watermark(
    mark_text,
    pagesize=(21 * cm, 29.7 * cm),
    font="Helvetica",
    font_size=30,
    font_color=(0, 0, 0),
    rotate=0,
    opacity=1,
    density=(5 * cm, 5 * cm),
):
    file_name = "/tmp/mark.pdf"
    c = canvas.Canvas(file_name, pagesize=pagesize)
    c.setFont(font, font_size)
    c.rotate(rotate)
    c.setStrokeColorRGB(0, 0, 0)
    r, g, b = font_color
    c.setFillColorRGB(r, g, b)
    c.setFillAlpha(opacity)

    row_gap, col_gap = density
    colN = int(pagesize[0] / col_gap)
    rowN = int(pagesize[1] / row_gap)
    x = colN * 4
    y = rowN * 4

    for i in range(y):
        for j in range(x):
            a = col_gap * (j - 2 * colN)
            b = row_gap * (i - 2 * rowN)
            c.drawString(a, b, mark_text)

    c.save()


def create_watermark(body):
    mark_text = body.get('watermark')
    # 1cm = 28.346456692913385， defalut is A4, (21*cm, 29.7*cm)
    pagesize = body.get("pagesize", [595.275590551181, 841.8897637795275])
    font = body.get("font", "Helvetica")
    font_size = body.get("font_size", 30)
    font_color = body.get("font_color", (0, 0, 0))
    rotate = body.get("rotate", 0)
    opacity = body.get("opacity", 0.1)
    # default is (7*cm, 10*cm)
    density = body.get("density", [198.4251968503937, 283.46456692913387])
    _create_watermark(
        mark_text, pagesize, font, font_size, font_color, rotate, opacity, density
    )
    print("create_watermark success!")


def download_pdf(url, local_path):
    """从给定URL下载PDF文件"""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"PDF downloaded successfully to {local_path}")

def upload_to_oss(bucket, local_file, object_name):
    """上传文件到OSS并返回预签名URL"""
    bucket.put_object_from_file(object_name, local_file)
    # 生成一个1小时有效的预签名URL
    url = bucket.sign_url('GET', object_name, 3600)
    return url

def handler(event, context):
    print(event)
    evt = json.loads(event)
    query_parameters = evt.get('queryParameters', {})
    pdf_url = query_parameters.get('pdf_url')
    body = json.loads(evt.get('body', '{}'))

    # 设置OSS客户端
    auth = oss2.StsAuth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET, OSS_SECURITY_TOKEN)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET)

    # 下载PDF文件
    local_pdf_file = "/tmp/input.pdf"
    try:
        download_pdf(pdf_url, local_pdf_file)
    except Exception as err:
        return {"code": "Failed", "message": f"Failed to download PDF: {str(err)}"}

    # 创建水印
    create_watermark(body)

    # 添加水印
    local_pdf_out_file = "/tmp/output.pdf"
    add_watermark(local_pdf_file, "/tmp/mark.pdf", local_pdf_out_file)
    print("PDF watermark added successfully!")

    # 上传到OSS并获取预签名URL
    try:
        object_name = f"watermarked_pdfs/{uuid.uuid4()}.pdf"
        presigned_url = upload_to_oss(bucket, local_pdf_out_file, object_name)
    except Exception as err:
        return {"code": "Failed", "message": f"Failed to upload to OSS: {str(err)}"}

    # 清理临时文件
    os.remove(local_pdf_file)
    os.remove(local_pdf_out_file)
    os.remove("/tmp/mark.pdf")

    return {
        "code": "Success",
        "message": "PDF processed and uploaded successfully",
        "presigned_url": presigned_url
    }
