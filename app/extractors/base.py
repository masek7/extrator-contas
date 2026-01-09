# app/extractors/base.py

def get_empty_data():
    """
    Retorna o esqueleto padrão de dados para Contas de Consumo.
    Todo extrator (Claro, Light, Vivo) deve preencher e retornar este dicionário.
    """
    return {
        "arquivo": None,              # Nome do arquivo PDF
        "fornecedor": "DESCONHECIDO", # Nome padronizado: CLARO, LIGHT, VIVO
        "cnpj_fornecedor": None,      # CNPJ da empresa emissora
        "data_emissao": None,         # Formato DD/MM/AAAA
        "data_vencimento": None,      # Formato DD/MM/AAAA
        "valor_total": 0.0,           # Float puro (ex: 150.50)
        "codigo_barras": None,        # Linha digitável para pagamento
        "status_leitura": "⚠️ Pendente", # Sucesso, Aviso ou Erro
        "log_erro": ""                # Detalhe técnico se falhar
    }