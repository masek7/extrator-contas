import re

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
       

        barcode = re.compile(r'\d{47,48}')
        barcode_nota = barcode.findall(doc)
        bc_format = barcode_nota[0]

        
        return bc_format
    
    except Exception as e:
        return None
    


    