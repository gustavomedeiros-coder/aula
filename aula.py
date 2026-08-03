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
    df = pd.read_csv(url)
    return df


df = carregar_dados()


# Visualização inicial
st.subheader("Dados")

st.dataframe(df.head())
