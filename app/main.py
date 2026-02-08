import streamlit as st
import pandas as pd
import io
from app import service

st.set_page_config(page_title="Extrator de Contas", layout="wide")
st.title("Extrator de Contas")


if 'dados_extraidos' not in st.session_state:
    st.session_state['dados_extraidos'] = None


uploaded_files = st.file_uploader(
    "Arraste seus PDFs aqui", 
    type="pdf", 
    accept_multiple_files=True
)


if uploaded_files and st.button("Processar Arquivos", type="primary"):
    with st.spinner(f"Processando {len(uploaded_files)} arquivos..."):
        
        lista_resultados = []
        
        
        for file in uploaded_files:
            try:
               
                file.seek(0)
                
                data = service.process_pdf(file)
                
                
                data['arquivo'] = file.name
                
                lista_resultados.append(data)
                
            except Exception as e:
                
                lista_resultados.append({
                    "arquivo": file.name,
                    "status_leitura": "Erro Crítico",
                    "log_erro": str(e)
                })
        
        
        df = pd.DataFrame(lista_resultados)
        st.session_state['dados_extraidos'] = df


if st.session_state['dados_extraidos'] is not None:
    st.divider()
    st.subheader("Confira e Edite os Dados:")
    
   
    df_editado = st.data_editor(
        st.session_state['dados_extraidos'],
        num_rows="dynamic",
        use_container_width=True,
        key="editor_dados"
    )
    
    st.divider()
    st.subheader("Exportar Resultados")

    
    c1, c2, c3, c4 = st.columns([2, 3, 2, 1.5])
    
    with c1:
        formato = st.radio(
            "Escolha o formato:",
            ["Excel (.xlsx)", "CSV (.csv)"],
            horizontal=True,
            label_visibility="collapsed"
        )

    
    if formato == "CSV (.csv)":
        arquivo_para_download = df_editado.to_csv(index=False).encode('utf-8')
        nome_arquivo = "contas_extraidas.csv"
        tipo_mime = "text/csv"
        label_btn = " Baixar CSV"
    else:
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_editado.to_excel(writer, index=False, sheet_name='Dados')
        
        arquivo_para_download = buffer.getvalue()
        nome_arquivo = "contas_extraidas.xlsx"
        tipo_mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        label_btn = " Baixar Planilha"

    with c2:
        st.empty() 

    with c3:
        st.download_button(
            label=label_btn,
            data=arquivo_para_download,
            file_name=nome_arquivo,
            mime=tipo_mime,
            use_container_width=True
        )

    with c4:
        if st.button("Limpar", type="primary", use_container_width=True):
            st.session_state['dados_extraidos'] = None
            st.rerun()