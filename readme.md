# Extrator de Dados de Notas Fiscais (PDF)

Uma aplicação web desenvolvida em Python para automatizar a extração de informações financeiras (CNPJ, Data, Valor Total) de notas fiscais em formato PDF.

O projeto resolve o problema de digitação manual de notas, permitindo upload em lote e exportação estruturada para CSV e XLSX.

## Tecnologias Utilizadas
* **Linguagem:** Python 3.10+
* **Interface:** Streamlit
* **Manipulação de PDF:** PyMuPDF (Fitz)
* **Processamento de Dados:** Pandas & Regex

## Funcionalidades Atuais (v1.0)
* [x] Upload de múltiplos arquivos PDF simultaneamente.
* [x] Extração inteligente de **Valor Total** (Lógica baseada em maior valor monetário).
* [x] Identificação automática de **CNPJ** e **Data de Emissão**.
* [x] Interface de tabela editável (Data Editor) para correções manuais rápidas.
* [x] Exportação dos dados consolidados para **CSV**.
* [x] Identificação visual de arquivos problemáticos.

## Roadmap (Próximos Passos)
A evolução planejada para o projeto inclui:
* [ ] **Integração com OCR (Tesseract):** Para ler notas escaneadas/fotos que não possuem camada de texto.
* [x] **Exportação Excel (.xlsx):** Para manter a formatação financeira nativa.
* [ ] **Validação de CNPJ:** Checkagem matemática de dígitos verificadores.
* [ ] **Dashboard Analítico:** Gráficos de gastos por período no próprio app.
* [ ] **Validação de CNPJ com API** Verifica se o CNPJ está ativo
