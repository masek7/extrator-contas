import re  
from app.extractors.base import get_empty_data

CNPJS_CONHECIDOS =[ 
                   
                   "71.208.516/0165-00",
                   "71.208.516/0001-74"
                   ]


def match(doc):
    text_clean = doc.replace(".", "").replace("/", "").replace("-", "")
    
    for cnpj in CNPJS_CONHECIDOS:
        cnpj_clean = cnpj.replace(".", "").replace("/", "").replace("-", "")
        
        if cnpj_clean in text_clean:
            return True
    
    return False

    

def cnpj_pagador(doc):
    #func que extrai o cnpj do pdf

    try:
        

        cnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}')
        cnpj_encontrado = cnpj.findall(doc)

        
        return cnpj_encontrado[0]
        
    except IndexError as e:
        return None
    

def cnpj_emitente(doc):
    #func que extrai o cnpj do pdf

    try:
        

        cnpj = re.compile(r'\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}')
        cnpj_encontrado = cnpj.findall(doc)

        
        return cnpj_encontrado[1]
        
    except IndexError as e:
        return None
    

def extract_value(doc):

    try:

        #func que extrai o valor contido na nota
        padrao = re.compile(r"\b\d+(?:[.,]\d{3})*[.,]\d{2}\b")
        valores_encontrados = padrao.findall(doc)

        if not valores_encontrados:
            return None
        
        valores_validos = []

        for valor in valores_encontrados:
            try:
                valor_limpo = valor
                
                if "," in valor_limpo and "." in valor_limpo:
                    if valor_limpo.rfind(",") > valor_limpo.rfind("."):
                        valor_limpo = valor_limpo.replace(".", "").replace(",", ".")
                    else:
                        valor_limpo = valor_limpo.replace(",", "")
                elif "," in valor_limpo:
                    valor_limpo = valor_limpo.replace(",", ".")
                elif "." in valor_limpo:
                    if len(valor_limpo.split(".")[-1]) == 2:
                        valor_limpo = valor_limpo
                    else:
                        valor_limpo = valor_limpo.replace(".", "")
                
                valor_float = float(valor_limpo)
                valores_validos.append(valor_float)
            except ValueError:
                continue
            
        if not valores_validos:
            return None
            
    
        valor_maximo = max(valores_validos)
        return valor_maximo
            

    except Exception as e:
        return None
    


def expire_date(doc):
    
    try:

        #func que extrai a data contida na nota
       

        data = re.compile(r'\d{2}\/\d{2}\/\d{4}')
        data_nota = data.findall(doc)
        exd_format = data_nota[0]

        
        return exd_format
    
    except Exception as e:
        return None
    

def emission_date(doc):
    
    try:

        #func que extrai a data contida na nota
       

        data = re.compile(r'\d{2}\/\d{2}\/\d{4}')
        data_nota = data.findall(doc)
        ed_format = data_nota[1]

        
        return ed_format
    
    except Exception as e:
        return None
    

def barcode(doc):
    
    try:

        #func que extrai o codigo de barras contida na nota
       
        padrao = re.compile(r'(?:\d{11,13}-\d)(?:\s+\d{11,13}-\d)+')
        encontrado = padrao.search(doc)

        if not encontrado:
            return None

        return encontrado.group(0).replace("-", "").replace(" ", "").strip()
    except Exception as e:
        return None
    

def nota_number(doc):
    
    try:

        #func que extrai o numero da nota contida na nota
       

        nota = re.compile(r'\b\d{6,10}\b')
        nota_nota = nota.findall(doc)
        nn_format = nota_nota[0]

        
        return nn_format
    
    except Exception as e:
        return None


def extract(doc_text):
    """
    Função Mestra: O Services.py chama AQUI.
    Ela organiza os dados no padrão do sistema.
    """
    # 1. Pega o formulário em branco
    data = get_empty_data()
    
    # 2. Preenche os metadados
    data['arquivo'] = "Processado via Algar"
    data['fornecedor'] = "ALGAR TELECOM"
    
    # 3. Chama suas funções especialistas
    # Note que passamos 'doc_text' para todas elas
    data['cnpj_fornecedor'] = cnpj_emitente(doc_text)
    data['data_emissao']    = emission_date(doc_text)
    data['data_vencimento'] = expire_date(doc_text)
    data['valor_total']     = extract_value(doc_text)
    data['codigo_barras']   = barcode(doc_text)
    
    # Opcional: Pegar o número da nota se quiser salvar no Excel
    # Você pode adicionar um campo 'numero_nota' no base.py depois se quiser
    # data['numero_nota'] = nota_number(doc_text) 

    # 4. Validação Final de Qualidade
    if data['valor_total'] and data['data_vencimento']:
        data['status_leitura'] = "✅ Sucesso"
    else:
        missing = []
        if not data['valor_total']: missing.append("Valor")
        if not data['data_vencimento']: missing.append("Vencimento")
        data['status_leitura'] = f"⚠️ Aviso: Faltou {', '.join(missing)}"
        
    return data