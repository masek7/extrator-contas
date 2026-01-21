import fitz  # PyMuPDF
import os
import sys

# Garante que o Python encontre a pasta 'app'
sys.path.append(os.getcwd())

from app.extractors import vivo
from app.extractors import vivo

# ==========================================
# ⚙️ CONFIGURAÇÃO
# Coloque o nome do seu PDF aqui
ARQUIVO_PDF = "C:/Users/GuiMo/OneDrive/NOTAS_TESTE/VIVO_MODEL2.pdf" 
# ==========================================

def run_lab():
    print(f"--- 🧪 Iniciando Laboratório de Integração: {ARQUIVO_PDF} ---")

    if not os.path.exists(ARQUIVO_PDF):
        print(f"❌ ERRO: O arquivo '{ARQUIVO_PDF}' não foi encontrado.")
        return

    # 1. Leitura do Texto (Simulando o que o Service faz)
    try:
        doc = fitz.open(ARQUIVO_PDF)
        texto_completo = ""
        for page in doc:
            texto_completo += page.get_text() + "\n"
    except Exception as e:
        print(f"❌ Erro ao ler PDF: {e}")
        return

    print("--- 1. TESTE DE IDENTIDADE (MATCH) ---")
    
    # Chama a função match para ver se ele reconhece o CNPJ
    e_vivo = vivo.match(texto_completo)
    
    if e_vivo:
        print(f"✅ Identificado como VIVO! (Match = True)")
        print(f"-> O sistema iria redirecionar para vivo.py corretamente.")
        print(f"Aqui esta o texto extraído do PDF:\n{texto_completo}")
    else:
        print(f"❌ FALHA: O vivo.py disse que NÃO é uma conta da Vivo.")
        print("-> Verifique se o CNPJ no topo do vivo.py está correto.")
        print("-> Verifique se o OCR leu o CNPJ corretamente no texto cru.")
        return # Para o teste se não reconhecer

    print("\n--- 2. TESTE DE EXTRAÇÃO COMPLETA (EXTRACT) ---")
    
    # Chama a função Mestra que você acabou de criar
    try:
        resultado = vivo.extract(texto_completo)
        
        # Mostra o resultado formatado
        for chave, valor in resultado.items():
            # Formatação bonita para alinhar o texto
            print(f"{chave.ljust(20)}: {valor}")
            
    except Exception as e:
        print(f"❌ Erro fatal na função extract: {e}")

if __name__ == "__main__":
    run_lab()