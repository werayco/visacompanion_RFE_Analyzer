import fitz
from docx import Document
import os


class petitionLoaders:
    @staticmethod
    def extract_text_from_docx(docx_path: str) -> str:
        doc = Document(docx_path)
        return " ".join([para.text for para in doc.paragraphs])

    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip() if text.strip() else "No extractable text found."

    @staticmethod
    def extract_text_from_txt(txt_path: str) -> str:
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            with open(txt_path, "r", encoding="ISO-8859-1") as f:
                return f.read()

    @staticmethod
    def extract_text_from_file(file_path):
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == ".pdf":
            return petitionLoaders.extract_text_from_pdf(file_path)
        elif ext == ".txt":
            return petitionLoaders.extract_text_from_txt(file_path)
        elif ext == ".docx":
            return petitionLoaders.extract_text_from_docx(file_path)
        else:
            return "Unsupported file format!"
