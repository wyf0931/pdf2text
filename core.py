import pytesseract
import pdf2image
from PIL import Image
from utils import get_file_path
from models import Page, Pdf, Task
from flask import current_app
import fitz


def extract(pdf_hash: str) -> None:
    pdf_path = get_file_path(pdf_hash)
    pdf = Pdf.get_by_hash(pdf_hash)
    next_page = Page.get_max_page_num(pdf.id) + 1

    doc = fitz.open(pdf_path)

    scanned_flag = []
    for page_num in range(doc.page_count):
        scanned_flag.append(is_page_scanned(doc, page_num))

    images = pdf2image.convert_from_path(pdf_path)

    for page_num in range(next_page, doc.page_count):
        try:
            text = ''
            if scanned_flag[page_num]:
                # ocr
                image = images[page_num]
                text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            else:
                # extract
                page = doc.load_page(page_num)
                text = page.get_text()

            page = Page(pdf_id=pdf.id, page_num=page_num, page_content=text)
            Page.save(page)
            current_app.logger.info(
                f'extract page success, pdf_hash={pdf_hash}, current_page_num={page_num}, is_scanned={scanned_flag[page_num]}')
        except Exception as e:
            current_app.logger.error('extract pdf text fail.', stack_info=True)

    doc.close()


def is_page_scanned(doc, page_num):
    page = doc.load_page(page_num)
    images = page.get_images()
    return len(images) == 1
