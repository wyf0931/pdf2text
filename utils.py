from PyPDF2 import PdfReader
import fitz
import pytesseract
import pdf2image
from flask import current_app
import os


def get_page_num(pdf_path) -> int:
    # Using PyPDF2 to extract text
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            return len(pdf_reader.pages)
    except Exception as e:
        current_app.logger.error(f"Error: {e}")

    # Using PyMuPDF (fitz) to extract images
    try:
        pdf_document = fitz.open(pdf_path)
        return pdf_document.page_count
    except Exception as e:
        current_app.logger.error(f"Error: {e}")

    return -1


def is_scanned_pdf(pdf_path):
    # Check if the PDF contains any scanned images
    scanned = False

    # Using PyPDF2 to extract text
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text.strip():  # If extracted text is not empty, it's likely not scanned
                    return False
    except Exception as e:
        print(f"Error: {e}")
        pass  # Handle encrypted or corrupted PDFs

    # Using PyMuPDF (fitz) to extract images
    try:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            images = page.get_images(full=True)
            if images:
                scanned = True
                break
    except Exception as e:
        print(f"Error: {e}")

    return scanned

# 从扫描的pdf文件中提取文本内容
def extract_text_from_scanned_pdf(pdf_path):

    # Convert PDF to a list of images
    images = pdf2image.convert_from_path(pdf_path)
    
    # Initialize an empty string to store text
    extracted_text = ''
    
    # Loop through images and apply OCR
    for image in images:
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        extracted_text += text + '\n'  # Separate text from different images with a newline

    return extracted_text


def get_file_path(pdf_hash):
    temp_dir = './data/'
    filename = f"{pdf_hash}.pdf"
    pdf_path = os.path.join(temp_dir, filename)
    return pdf_path



# print(is_scanned_pdf('/Users/scott/Desktop/001.pdf'))
