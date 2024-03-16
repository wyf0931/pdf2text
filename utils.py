import fitz
from flask import current_app
import os


def get_page_num(pdf_path) -> int:
    try:
        pdf_document = fitz.open(pdf_path)
        total_pages = pdf_document.page_count
        pdf_document.close()
        return total_pages
    except Exception as e:
        current_app.logger.error(f"Error: {e}")
    return -1


def get_file_path(pdf_hash):
    temp_dir = './data/'
    filename = f"{pdf_hash}.pdf"
    pdf_path = os.path.join(temp_dir, filename)
    return pdf_path