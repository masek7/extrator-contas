# app/service.py
import fitz
from app.extractors import algar, vivo, base, boleto 
def process_pdf(file_stream):
    try:
        
        doc = fitz.open(stream=file_stream.read(), filetype="pdf")
        text_content = ""
        for page in doc:
            text_content += page.get_text() + "\n"
    except Exception as e:
        return {
            "status_leitura": "Erro Leitura",
            "log_erro": str(e)
        }

    
    text_upper = text_content.upper()

    if algar.match(text_content):
        return algar.extract(text_content)
    elif vivo.match(text_content):
        return vivo.extract(text_content)
    else:
        
        return boleto.extract(text_content)