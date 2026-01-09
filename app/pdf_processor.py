from pathlib import Path
import pymupdf as fitz


def process_pdf(pdf_file):

    #funcao que processa o pdf e extrai o texto da primeira pagina
    read_pdf = pdf_file.read()

    try:
        
        doc = fitz.open(stream= read_pdf, filetype="pdf")

        all_pages_text = []
        for page in doc:
            text_content = page.get_text()  # Extrai todo o texto da pagina especifica
            all_pages_text.append(text_content)

        return {
            "status": "success",
            "filename": pdf_file.name,
            "content": "".join(all_pages_text)
        }

    except Exception as e:
        return {
            "status": "error",
            "filename": getattr (pdf_file, 'name', 'desconhecido'),
            "message": str(e)
        }
        
       
    
