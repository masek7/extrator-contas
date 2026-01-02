from pdf_processor import process_pdf
from data_extractor import extract_cnpj, extract_value, extract_date


def analyze_pdf(pdf_file):
    # Função que analisa o PDF e extrai as informações desejadas
    
    processed_pdf = process_pdf(pdf_file)

    if processed_pdf["status"] == "error":
        return {
            "status": "error",
            "message": processed_pdf["message"]
        }
    

    cnpj = extract_cnpj(processed_pdf["content"])
    date = extract_date(processed_pdf["content"])
    value = extract_value(processed_pdf["content"])

    return {
        "filename": processed_pdf["filename"],
        "status": "success",
        "dados": {
        "STATUS" : "",
        "CNPJ": cnpj,
        "DATA": date,
        "VALOR": value
        }
    }
