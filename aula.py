import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Configuração da página
st.set_page_config(
    page_title="Meu Dashboard",
    layout="wide"
)


# Título
st.title("📊 Meu Dashboard")


# Carregar dados
url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.25418/dados?formato=csv"


@st.cache_data
def carregar_dados():
    df = pd.read_csv(
        url,
        sep=";",
        decimal=","
    )
    return df


df = carregar_dados()


# Visualização inicial
st.subheader("Dados")

st.dataframe(df.head())

#a partir daqui são gráficos
st.subheader("Série temporal")

fig, ax = plt.subplots(figsize=(12,6))

ax.plot(
    df["data"],
    df["valor"]
)

ax.set_title(
    "Série temporal"
)

ax.grid(
    linestyle="--",
    alpha=0.3
)

st.pyplot(fig)
