from pathlib import Path
import pymupdf as fitz


def process_pdf(pdf_file):

    #funcao que processa o pdf e extrai o texto da primeira pagina
    read_pdf = pdf_file.read()

    try:
        doc = fitz.open(stream= read_pdf, filetype="pdf")
        page = doc.load_page(0)  # Carrega a primeira página (índice 0)
        text_content = page.get_text()  # Extrai todo o texto da pagina especifica

        return {
            "status": "success",
            "filename": pdf_file.name,
            "content": text_content
        }

    except Exception as e:
        return {
            "status": "error",
            "filename": getattr (pdf_file, 'name', 'desconhecido'),
            "message": str(e)
        }
        
       
    
