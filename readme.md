# Extrator Automatizado de Contas de Consumo (Utility Bill Parser)

Uma ferramenta de Engenharia de Dados focada na extração, padronização e validação de informações de contas de consumo (Energia, Água, Telefonia/Internet) a partir de arquivos PDF.

O objetivo é eliminar a digitação manual no setor financeiro, gerando arquivos estruturados (Excel/CSV) prontos para importação em ERPs ou sistemas bancários.

## Problema Resolvido

Empresas recebem dezenas de faturas com layouts diferentes todos os meses.

* A conta da **Light** coloca o total no rodapé.
* A conta da **Claro** coloca o vencimento no topo.
* A conta da **Águas do Rio** usa termos diferentes.

Este projeto utiliza um padrão de projeto **Factory (Fábrica)** para identificar automaticamente a concessionária e aplicar o modelo de extração correto (Template-based Extraction).

## Funcionalidades Principais

* [✓] **Identificação Automática:** Detecta se o PDF é Light, Enel, Claro, Vivo, etc.
* [✓] **Padronização de Saída:** Independente do layout original, o Excel final tem sempre as mesmas colunas: `Fornecedor`, `Vencimento`, `Valor`, `Linha Digitável`.
* [✓] **Extração de Código de Barras:** Captura a linha digitável para pagamento.
* [✓] **Processamento em Lote:** Lê pastas inteiras com arquivos misturados.
* [ ] **Validação de Regras:** Verifica se a data de vencimento é futura ou passada (Alertas de juros).

## Stack

* **Linguagem:** Python 3.10+
* **Interface:** Streamlit (Front-end para upload e conferência)
* **Processamento:** PyMuPDF (Fitz)
* **Lógica:** Regex (Expressões Regulares avançadas por template)
* **Dados:** Pandas & OpenPyXL

## Estrutura do Projeto (Arquitetura)

O sistema opera com módulos extratores isolados para garantir precisão:

```text
├── app/
│   ├── templates/          # "Cérebros" individuais
│   │   ├── vivo.py         # Lógica exclusiva para faturas vivo
│   │   ├── algar.py        # Lógica exclusiva para faturas algar
│   │   └── boleto.py       # Lógica exclusiva para boletos genéricos (qualquer boleto)
│   ├── main.py             # Interface do Usuário
│   └── service.py          # Orquestrador do processamento 
