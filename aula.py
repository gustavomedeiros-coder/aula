import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------
# Configuração da página
# ---------------------------------------

st.set_page_config(
    page_title="IBCR-PE | Dashboard Econômico",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------
# Título
# ---------------------------------------

st.title("📊 Dashboard IBCR-PE")
st.caption(
    "Índice de Atividade Econômica de Pernambuco"
)


# ---------------------------------------
# Carregamento dos dados
# ---------------------------------------

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


# ---------------------------------------
# Gráfico 1 - Série temporal com média móvel
# ---------------------------------------

st.subheader("Série temporal com média móvel")


df["media_movel"] = df["valor"].rolling(
    window=12
).mean()


fig, ax = plt.subplots(
    figsize=(12,6)
)


ax.plot(
    df["data"],
    df["valor"],
    linewidth=1.5,
    alpha=0.6,
    label="IBCR-PE"
)


ax.plot(
    df["data"],
    df["media_movel"],
    linewidth=3,
    label="Média móvel (12 meses)"
)


ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Índice"
)


ax.grid(
    linestyle="--",
    alpha=0.3
)


ax.legend()


fig.tight_layout()


st.pyplot(fig)



# ---------------------------------------
# Gráfico 2 - Distribuição dos valores
# ---------------------------------------

st.subheader("Distribuição dos valores")


fig, ax = plt.subplots(
    figsize=(10,6)
)


ax.hist(
    df["valor"],
    bins=30,
    edgecolor="black"
)


ax.set_xlabel(
    "Valor"
)

ax.set_ylabel(
    "Frequência"
)


ax.grid(
    alpha=0.3
)


fig.tight_layout()


st.pyplot(fig)
