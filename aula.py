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

# -------------------------------------
# Gráfico 3 - Diagrama de caixa com média
# -------------------------------------

st.subheader("Diagrama de caixa com média")


# Criar gráfico
fig, ax = plt.subplots(
    figsize=(10, 5)
)


# Boxplot
ax.boxplot(
    df["valor"],
    vert=False,
    showmeans=True,
    patch_artist=True
)


# Título
ax.set_title(
    "Diagrama de caixa com média",
    fontsize=16,
    fontweight="bold"
)


# Eixo
ax.set_xlabel(
    "Valor"
)


# Grade
ax.grid(
    alpha=0.3
)


# Ajuste
fig.tight_layout()


# Exibir no Streamlit
st.pyplot(fig)

# -------------------------------------
# Gráfico 4 - Mapa de calor temporal
# -------------------------------------

st.subheader("Mapa de calor temporal")


# Criar ano e mês
df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month


# Organizar dados para o heatmap
heatmap_data = pd.pivot_table(
    df,
    values="valor",
    index="ano",
    columns="mes",
    aggfunc="mean"
)


# Criar gráfico
fig, ax = plt.subplots(
    figsize=(12, 6)
)


# Mapa de calor
imagem = ax.imshow(
    heatmap_data,
    aspect="auto"
)


# Barra de cores
fig.colorbar(
    imagem,
    ax=ax,
    label="Valor médio"
)


# Meses
ax.set_xticks(
    range(12)
)

ax.set_xticklabels(
    [
        "Jan","Fev","Mar","Abr",
        "Mai","Jun","Jul","Ago",
        "Set","Out","Nov","Dez"
    ]
)


# Anos
ax.set_yticks(
    range(len(heatmap_data.index))
)

ax.set_yticklabels(
    heatmap_data.index
)


# Título
ax.set_title(
    "Mapa de calor temporal",
    fontsize=16,
    fontweight="bold"
)


# Eixos
ax.set_xlabel(
    "Mês"
)

ax.set_ylabel(
    "Ano"
)


fig.tight_layout()


# Mostrar no Streamlit
st.pyplot(fig)

# -------------------------------------
# Gráfico 5 - Valor médio por ano
# -------------------------------------

st.subheader("Valor médio do IBCR-PE por ano")


# Calcular média anual
media_ano = df.groupby(
    df["data"].dt.year
)["valor"].mean()


# Criar gráfico
fig, ax = plt.subplots(
    figsize=(10, 6)
)


# Gráfico de barras horizontal
ax.barh(
    media_ano.index.astype(str),
    media_ano.values,
    edgecolor="black"
)


# Título
ax.set_title(
    "Valor médio por Ano",
    fontsize=16,
    fontweight="bold"
)


# Eixos
ax.set_xlabel(
    "Valor médio",
    fontsize=12
)

ax.set_ylabel(
    "Ano",
    fontsize=12
)


# Grade
ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.3
)


# Ajuste
fig.tight_layout()


# Exibir no Streamlit
st.pyplot(fig)
