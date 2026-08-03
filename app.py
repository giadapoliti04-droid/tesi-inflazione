import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione della pagina
st.set_page_config(page_title="Tesi Inflazione", layout="wide")

st.title("📊 Analisi dell'Inflazione: Eurozona, Albania e Venezuela")
st.markdown("Progetto di Tesi — Confronto interattivo dei tassi d'inflazione.")

# --- CARICAMENTO DATI ---
@st.cache_data
def carica_dati():
    # Legge il file CSV presente nella cartella (prova sia con virgola che con punto e virgola)
    try:
        df = pd.read_csv("inflazione-2.csv", sep=None, engine='python')
    except Exception:
        df = pd.read_csv("inflazione-2.csv")
    
    # Pulizia nomi colonne
    df.columns = [str(col).strip() for col in df.columns]
    
    # Convertiamo la prima colonna degli anni
    col_anno = df.columns[0]
    df[col_anno] = pd.to_numeric(df[col_anno], errors='coerce')
    df = df.dropna(subset=[col_anno])
    df[col_anno] = df[col_anno].astype(int)
    
    # Convertiamo le altre colonne in numeri
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
        
    return df, col_anno

try:
    df, col_anno = carica_dati()

    # --- SIDEBAR / CONTROLLI ---
    st.sidebar.header("⚙️ Opzioni e Filtri")

    # Bottone rapido COVID
    covid_pressed = st.sidebar.button("🦠 Focus Periodo COVID (2019-2022)")

    min_year = int(df[col_anno].min())
    max_year = int(df[col_anno].max())

    if covid_pressed:
        range_anni = (2019, 2022)
    else:
        range_anni = st.sidebar.slider(
            "Seleziona intervallo di Anni:",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )

    # Scelta Paesi / colonne disponibili
    colonne_paesi = [c for c in df.columns if c != col_anno]
    paesi_selezionati = st.sidebar.multiselect(
        "Seleziona Paesi / Aree da confrontare:",
        options=colonne_paesi,
        default=colonne_paesi
    )

    # Checkbox scala logaritmica
    usa_log = st.sidebar.checkbox(
        "📐 Usa scala logaritmica (consigliato per il Venezuela)", 
        value=False
    )

    # --- FILTRAGGIO DATI ---
    df_filtered = df[(df[col_anno] >= range_anni[0]) & (df[col_anno] <= range_anni[1])]

    # --- GRAFICO ---
    if paesi_selezionati:
        st.subheader(f"📈 Tasso di Inflazione ({range_anni[0]} - {range_anni[1]})")

        fig = px.line(
            df_filtered,
            x=col_anno,
            y=paesi_selezionati,
            markers=True,
            labels={"value": "Inflazione (%)", col_anno: "Anno", "variable": "Paese / Area"},
            log_y=usa_log
        )

        fig.update_layout(
            hovermode="x unified",
            legend_title_text="Paese / Area",
            xaxis=dict(dtick=1),
            font=dict(size=14)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Tabella Dati
        with st.expander("📄 Mostra dati in formato tabella"):
            st.dataframe(df_filtered[[col_anno] + paesi_selezionati], use_container_width=True)

    else:
        st.warning("⚠️ Seleziona almeno un Paese dal menu a sinistra per generare il grafico.")

except Exception as e:
    st.error(f"⚠️ Si è verificato un errore nel caricamento del file `inflazione-2.csv`: {e}")
