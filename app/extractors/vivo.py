import re  
from app.extractors.base import get_empty_data
CNPJS_CONHECIDOS =[ 
    "02.558.157/0001-62", # Matriz SP
    "02.558.157/0002-43",
    "02.558.157/0003-24",
    "02.558.157/0004-05",
    "02.558.157/0005-96",
    "02.449.992/0001-64"  # Vivo/GVT antiga
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
    



def expire_date_m2(doc):
    
    try:

        #func que extrai a data contida na nota
       

        data = re.compile(r'\d{2}\/\d{2}\/\d{4}')
        data_nota = data.findall(doc)
        exd_format = data_nota[3]

        
        return exd_format
    
    except Exception as e:
        return None

def emission_date(doc):
    
    try:

        #func que extrai a data contida na nota
       

        data = re.compile(r'\d{2}\/\d{2}\/\d{4}')
        data_nota = data.findall(doc)
        ed_format = data_nota[3]

        
        return ed_format
    
    except Exception as e:
        return None
    

def emission_date_m2(doc):
    
    try:

        #func que extrai a data contida na nota
       

        data = re.compile(r'\d{2}\/\d{2}\/\d{4}')
        data_nota = data.findall(doc)
        ed_format = data_nota[0]

        
        return ed_format
    
    except Exception as e:
        return None

def barcode(doc):
    
   try:
       
        padrao = re.compile(r'\b\d{11,12}\s+\d{11,12}\s+\d{11,12}\s+\d{11,12}\b')
        
        encontrado = padrao.search(doc)

        if not encontrado:
            return None

        # LIMPEZA CRUCIAL:
        # Pega o texto encontrado (que tem quebras de linha e espaços)
        texto_sujo = encontrado.group(0)
        
        # Remove quebras de linha (\n), espaços e traços (se tiver sobrado algum)
        codigo_limpo = texto_sujo.replace("\n", "").replace(" ", "").replace("-", "").strip()
        
        return codigo_limpo
   except Exception as e:
        return None
   

def _barcode_novo(doc):
    try:
       
        regex_str = r'\b\d{11}\s+\d\s+\d{11}\s+\d\s+\d{11}\s+\d\s+\d{11}\s+\d\b'
        
        padrao = re.compile(regex_str)
        match = padrao.search(doc)

        if not match:
            return None
        texto_sujo = match.group(0)
        codigo_limpo = texto_sujo.replace(" ", "").replace("\n", "").strip()
        
        return codigo_limpo

    except Exception:
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


def _extract_layout_padrao(doc_text):
    """Layout Clássico (NFST) - Baseado no MODEL1.txt"""
    print("-> ⚙️ Processando com extrator: VIVO PADRÃO (NFST)")
    data = get_empty_data()
    data['arquivo'] = "Vivo - Layout Padrão (NFST)"
    data['fornecedor'] = "VIVO"
    
    # Reutiliza as funções que você já fez (assumindo que elas funcionam pro Mod 1)
    data['cnpj_fornecedor'] = cnpj_emitente(doc_text)
    data['data_emissao']    = emission_date(doc_text)
    data['data_vencimento'] = expire_date(doc_text)
    data['valor_total']     = extract_value(doc_text) # Sua função antiga
    data['codigo_barras']   = barcode(doc_text)

    if data['valor_total'] and data['data_vencimento']:
        data['status_leitura'] = "✅ Sucesso"
    else:
        missing = []
        if not data['valor_total']: missing.append("Valor")
        if not data['data_vencimento']: missing.append("Vencimento")
        data['status_leitura'] = f"⚠️ Aviso: Faltou {', '.join(missing)}"
    
    return data


def _extract_layout_novo(doc_text):
    """Layout Novo (NFCom) - Baseado no MODEL2.txt"""
    print("-> 🆕 Processando com extrator: VIVO NOVO (NFCom)")
    data = get_empty_data()
    data['arquivo'] = "Vivo - Layout Digital (NFCom)"
    data['fornecedor'] = "VIVO"

    # Lógica específica para o Layout 2
    data['cnpj_fornecedor'] = cnpj_emitente(doc_text)
    
    # No novo, Data de Emissão costuma vir perto de "Data de Emissão:" explícito
    # Adapte se necessário, mas o regex genérico costuma funcionar
    data['data_emissao']    = emission_date_m2(doc_text)
    data['data_vencimento'] = expire_date_m2(doc_text)
    
    # O valor total tem um padrão levemente diferente no novo
    data['valor_total']     = extract_value(doc_text)
    
    # O código de barras geralmente é igual, mas se falhar, crie um _barcode_novo
    data['codigo_barras']   = _barcode_novo(doc_text) 

    if data['valor_total'] and data['data_vencimento']:
        data['status_leitura'] = "✅ Sucesso"
    else:
        missing = []
        if not data['valor_total']: missing.append("Valor")
        if not data['data_vencimento']: missing.append("Vencimento")
        data['status_leitura'] = f"⚠️ Aviso: Faltou {', '.join(missing)}"

    return data



def extract(doc_text):
    # 1. Normaliza para busca
    text_upper = doc_text.upper()
    
    # 2. Verifica a Assinatura Digital do Layout Novo
    # confirma a presença de "NFCOM" no layout novo
    # confirma a frase "NOVO VISUAL"
    if "NFCOM" in text_upper or "NOVO VISUAL" in text_upper:
        return _extract_layout_novo(doc_text)
        
    # 3. Se não tiver os sinais acima, assume que é o antigo
    else:
        return _extract_layout_padrao(doc_text)