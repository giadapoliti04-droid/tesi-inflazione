import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analisi Inflazione - Tesi", layout="wide")

st.title("📊 Analisi dell'Inflazione: Italia, Sicilia, Lombardia, Eurozona e Venezuela")
st.write("Progetto di Tesi – Confronto interattivo dei dati regionali e internazionali.")

# Puntiamo direttamente al tuo nuovo file Excel caricato su GitHub
NOME_FILE = "dati.xlsx"

@st.cache_data
def carica_dati(filename):
    return pd.read_excel(filename)

try:
    df = carica_dati(NOME_FILE)
    
    st.sidebar.header("Opzioni e Filtri")
    
    colonne = df.columns.tolist()
    col_anno = next((c for c in colonne if 'anno' in c.lower() or 'year' in c.lower()), colonne[0])
    regioni_disponibili = [c for c in colonne if c != col_anno]
    
    regioni_selezionate = st.sidebar.multiselect(
        "Seleziona Aree / Paesi da confrontare:", 
        regioni_disponibili, 
        default=regioni_disponibili
    )
    
    usa_log = st.sidebar.checkbox("Usa scala logaritmica (consigliato in presenza di valori molto alti come il Venezuela)")

    st.subheader("Tasso di Inflazione per Area")
    
    if regioni_selezionate:
        fig = px.line(df, x=col_anno, y=regioni_selezionate, markers=True, title="Confronto Tassi")
        fig.update_layout(xaxis_title="Anno", yaxis_title="Valore (%)")
        
        if usa_log:
            fig.update_yaxes(type="log")
            
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Seleziona almeno un'area dalla barra laterale.")

    with st.expander("Mostra dati in formato tabella"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Errore nel caricamento del file: {e}. Assicurati che il file '{NOME_FILE}' si trovi nel repository di GitHub.")