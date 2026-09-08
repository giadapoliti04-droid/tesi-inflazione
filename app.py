import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analisi Inflazione - Tesi", layout="wide")

st.title("📊 Analisi dell'Inflazione: Italia, Sicilia e Lombardia")
st.write("Progetto di Tesi – Confronto interattivo dei dati regionali e nazionali.")

# Caricamento file Excel o CSV
uploaded_file = st.file_uploader("Carica il tuo file Excel", type=["xlsx", "csv"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.sidebar.header("Opzioni e Filtri")
    
    colonne = df.columns.tolist()
    
    # Identifica automaticamente la colonna dell'anno (cerca parole come 'anno' o 'year')
    col_anno = next((c for c in colonne if 'anno' in c.lower() or 'year' in c.lower()), colonne[0])
    
    # Le altre colonne sono le regioni/paesi (es. Italia, Sicilia, Lombardia)
    regioni_disponibili = [c for c in colonne if c != col_anno]
    
    # Filtro nella sidebar per scegliere quali regioni visualizzare nel grafico
    regioni_selezionate = st.sidebar.multiselect(
        "Seleziona Aree / Regioni da confrontare:", 
        regioni_disponibili, 
        default=regioni_disponibili
    )
    
    usa_log = st.sidebar.checkbox("Usa scala logaritmica")

    # Generazione del grafico con le tue colonne reali
    st.subheader("Tasso di Inflazione per Area")
    
    if regioni_selezionate:
        # Plotly traccia automaticamente ogni colonna selezionata come una linea distinta
        fig = px.line(df, x=col_anno, y=regioni_selezionate, markers=True, title="Confronto Tassi")
        fig.update_layout(xaxis_title="Anno", yaxis_title="Valore (%)")
        
        if usa_log:
            fig.update_yaxes(type="log")
            
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Seleziona almeno una regione dalla barra laterale.")

    with st.expander("Mostra dati in formato tabella"):
        st.dataframe(df)
else:
    st.info("Carica il file Excel con i dati di Italia, Sicilia e Lombardia per iniziare.")
