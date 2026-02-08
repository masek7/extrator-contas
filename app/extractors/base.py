# app/extractors/base.py

def get_empty_data():
    """
    Retorna o esqueleto padrão de dados para Contas de Consumo.
    Todo extrator (Claro, Light, Vivo) deve preencher e retornar este dicionário.
    """
    return {
        "arquivo": None,              
        "fornecedor": "DESCONHECIDO", 
        "cnpj_fornecedor": None,      
        "data_emissao": None,         
        "data_vencimento": None,      
        "valor_total": 0.0,           
        "codigo_barras": None,        
        "status_leitura": "Pendente", 
        "log_erro": ""                
    }