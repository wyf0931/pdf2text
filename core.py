import pytesseract
import pdf2image
from utils import get_file_path, is_scanned_pdf
from models import Page, Pdf, Task
from flask import current_app

def extract(pdf_hash: str) -> None:
    pdf_path = get_file_path(pdf_hash)
    if is_scanned_pdf(pdf_path):
        scanned_pdf_to_text(pdf_hash)
    else:
        current_app.logger.warning('unsupported file type.')
        pass


def scanned_pdf_to_text(pdf_hash: str) -> None:
    pdf_path = get_file_path(pdf_hash)

    pdf = Pdf.get_by_hash(pdf_hash)

    next_page = Page.get_max_page_num(pdf.id) + 1

    # Convert PDF to a list of images
    images = pdf2image.convert_from_path(pdf_path)

    # Initialize an empty string to store text
    # extracted_text = ''

    # Loop through images and apply OCR
    for i in range(next_page, len(images)):
        image = images[i]
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        page = Page(pdf_id=pdf.id, page_num=i, page_content=text)
        Page.save(page)
        current_app.logger.info(f'extract page success, pdf_hash={pdf_hash}, current_page_num={i}')
