import io
import PyPDF2
import docx2txt
from fastapi import HTTPException, UploadFile

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """استخراج النص من ملفات PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        return extracted_text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"فشل في قراءة ملف الـ PDF: {str(e)}"
        )

def extract_text_from_docx(file_bytes: bytes) -> str:
    """استخراج النص من ملفات Word (DOCX)"""
    try:
        extracted_text = docx2txt.process(io.BytesIO(file_bytes))
        return extracted_text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"فشل في قراءة ملف الـ Word: {str(e)}"
        )

async def parse_resume_file(file: UploadFile) -> str:
    """التحقق من امتداد الملف وتوجيهه للدالة المناسبة"""
    filename = file.filename.lower()
    content = await file.read()