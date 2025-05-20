import os
import PyPDF2

def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def parse_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return read_txt(file_path)
    elif ext == '.pdf':
        return read_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

if __name__ == '__main__':
    txt='C:\\Users\\dipak\\AppData\\Local\\Temp\\tmpuikfmxf6'
    print(parse_file(txt))




