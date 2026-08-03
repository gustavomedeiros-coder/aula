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

    df["data"] = pd.to_datetime(
        df["data"],
        dayfirst=True
    )

    return df


df = carregar_dados()

st.write(df.columns)

# Visualização inicial
st.subheader("Dados")

st.dataframe(df.head())

#a partir daqui são gráficos
# -------------------------------------
# Gráfico 1 - Série temporal com média móvel
# -------------------------------------

st.subheader("Séries temporais com média móvel")


# Criar média móvel (12 períodos = meses)
df["media_movel"] = df["valor"].rolling(
    window=12
).mean()


# Criar gráfico
fig, ax = plt.subplots(figsize=(12, 6))


# Série original
ax.plot(
    df["data"],
    df["valor"],
    linewidth=1.5,
    alpha=0.6,
    label="Original"
)


# Média móvel
ax.plot(
    df["data"],
    df["media_movel"],
    linewidth=3,
    label="Média Móvel (12)"
)


# Título
ax.set_title(
    "Séries temporais com média móvel",
    fontsize=16,
    fontweight="bold"
)


# Eixos
ax.set_xlabel(
    "Data",
    fontsize=12
)

ax.set_ylabel(
    "IBCR-PE",
    fontsize=12
)


# Grade
ax.grid(
    linestyle="--",
    alpha=0.3
)


# Legenda
ax.legend()


# Ajuste
fig.tight_layout()


# Exibir no Streamlit
st.pyplot(fig)
