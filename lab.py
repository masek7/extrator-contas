import os
import fitz  # PyMuPDF
from app import service

# --- CONFIGURAÇÃO ---
# Troque pelo nome do arquivo que você quer investigar
NOME_DO_ARQUIVO = "C:/Users/GuiMo/OneDrive/NOTAS_TESTE/BOLETO_1.pdf" 

def rodar_teste():
    print(f"\n🧪 --- LABORATÓRIO DE DEBUG: {NOME_DO_ARQUIVO} ---")

    if not os.path.exists(NOME_DO_ARQUIVO):
        print(f"❌ Erro: Arquivo '{NOME_DO_ARQUIVO}' não encontrado.")
        return

    # Abre o arquivo
    with open(NOME_DO_ARQUIVO, "rb") as arquivo_pdf:
        
        # ---------------------------------------------------------
        # PASSO 1: ESPIÃO (Lê o texto cru para você ver)
        # ---------------------------------------------------------
        print("\n📝 TEXTO EXTRAÍDO (RAW TEXT):")
        print("-" * 50)
        
        # Lemos o conteúdo em bytes para o PyMuPDF
        conteudo_bytes = arquivo_pdf.read()
        doc = fitz.open(stream=conteudo_bytes, filetype="pdf")
        
        texto_completo = ""
        for i, pagina in enumerate(doc):
            texto_pag = pagina.get_text()
            print(f"[PÁGINA {i+1}]")
            print(texto_pag)
            texto_completo += texto_pag + "\n"
            
        print("-" * 50)
        print(f"ℹ️  Tamanho do texto: {len(texto_completo)} caracteres.")

        # ---------------------------------------------------------
        # PASSO 2: O PROCESSAMENTO REAL
        # ---------------------------------------------------------
        # IMPORTANTE: Como já lemos o arquivo acima, o "cursor" está no final.
        # Precisamos voltar para o início (seek 0) para o service ler de novo.
        arquivo_pdf.seek(0)
        
        print("\n⚙️  RODANDO O EXTRATOR...")
        resultado = service.process_pdf(arquivo_pdf)

    # ---------------------------------------------------------
    # PASSO 3: EXIBIÇÃO DO RESULTADO FINAL
    # ---------------------------------------------------------
    print("\n📊 DADOS ESTRUTURADOS:")
    print("=" * 50)
    
    for chave, valor in resultado.items():
        # Formatação bonita
        print(f"🔑 {chave.ljust(20)} | {valor}")
        
    print("=" * 50)
    
    # Diagnóstico final
    fornecedor = resultado.get('fornecedor', 'DESCONHECIDO')
    if fornecedor == "GENERICO":
        print("⚠️  FALLBACK: O extrator GENÉRICO foi acionado.")
        print("   -> Dica: Copie o 'TEXTO EXTRAÍDO' acima e teste no regex101.com")
    elif fornecedor in ["VIVO", "ALGAR"]:
        print(f"✅ SUCESSO: O especialista da {fornecedor} assumiu.")
    else:
        print("❌ ERRO: Nenhum dado foi extraído corretamente.")

if __name__ == "__main__":
    rodar_teste()