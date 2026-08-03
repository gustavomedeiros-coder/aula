import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ======================================
# CONFIGURAÇÃO
# ======================================

st.set_page_config(
    page_title="IBCR-PE | Dashboard Econômico",
    page_icon="📊",
    layout="wide"
)


# ======================================
# ESTILO
# ======================================

plt.style.use("seaborn-v0_8-whitegrid")


# ======================================
# CABEÇALHO
# ======================================

st.title("📊 IBCR-PE — Indicador de Atividade Econômica")

st.markdown(
    """
    Dashboard interativo do **Índice de Atividade Econômica Regional de Pernambuco (IBCR-PE)**.

    O indicador acompanha a evolução da atividade econômica do estado,
    permitindo observar tendências, ciclos e mudanças estruturais.
    """
)


# ======================================
# DADOS
# ======================================

url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.25418/dados?formato=csv"


@st.cache_data
def carregar_dados():

    df = pd.read_csv(
        url,
        sep=";",
        decimal=","
    )

    df["data"] = pd.to_datetime(
        df["data"],
        dayfirst=True
    )

    df = df.sort_values(
        "data"
    )

    return df


df = carregar_dados()



# ======================================
# TRATAMENTO
# ======================================

df["media_movel"] = (
    df["valor"]
    .rolling(12)
    .mean()
)


df["ano"] = df["data"].dt.year

df["mes"] = df["data"].dt.month



# ======================================
# INDICADORES
# ======================================

ultimo_valor = df["valor"].iloc[-1]

media_historica = df["valor"].mean()

maximo = df["valor"].max()

minimo = df["valor"].min()



col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Último IBCR-PE",
        f"{ultimo_valor:.2f}"
    )


with col2:
    st.metric(
        "Média histórica",
        f"{media_historica:.2f}"
    )


with col3:
    st.metric(
        "Máximo histórico",
        f"{maximo:.2f}"
    )


with col4:
    st.metric(
        "Mínimo histórico",
        f"{minimo:.2f}"
    )


st.divider()

