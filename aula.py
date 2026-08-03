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
# BARRA LATERAL
# ======================================

st.sidebar.title("📊 IBCR-PE")

st.sidebar.markdown(
    """
    **Índice de Atividade Econômica Regional
    de Pernambuco**

    O IBCR-PE acompanha a evolução da
    atividade econômica do estado, servindo
    como indicador antecedente do PIB.
    """
)


st.sidebar.divider()


st.sidebar.subheader(
    "Período de análise"
)


data_inicial = st.sidebar.date_input(
    "Data inicial",
    df["data"].min()
)


data_final = st.sidebar.date_input(
    "Data final",
    df["data"].max()
)



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

# ======================================
# ABAS DO DASHBOARD
# ======================================

aba1, aba2, aba3, aba4 = st.tabs(
    [
        "📈 Evolução temporal",
        "📊 Distribuição",
        "🌡 Sazonalidade",
        "📅 Análise anual"
    ]
)


# ======================================
# ABA 1 - EVOLUÇÃO TEMPORAL
# ======================================

with aba1:

    st.subheader(
        "Evolução do IBCR-PE"
    )


    fig, ax = plt.subplots(
        figsize=(12,5)
    )


    # Série original
    ax.plot(
        df["data"],
        df["valor"],
        linewidth=1.5,
        alpha=0.6,
        label="IBCR-PE"
    )


    # Média móvel
    ax.plot(
        df["data"],
        df["media_movel"],
        linewidth=3,
        label="Média móvel (12 meses)"
    )


    # Destacar pandemia
    ax.axvspan(
        pd.Timestamp("2020-03-01"),
        pd.Timestamp("2021-12-01"),
        color="gray",
        alpha=0.2,
        label="Pandemia"
    )


    ax.set_title(
        "IBCR-PE e média móvel de 12 meses",
        fontsize=16,
        fontweight="bold"
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



# ======================================
# ABA 2 - DISTRIBUIÇÃO
# ======================================

with aba2:

    st.subheader(
        "Distribuição histórica do indicador"
    )


    col1, col2 = st.columns(2)


    # Histograma
    with col1:

        fig, ax = plt.subplots(
            figsize=(7,4)
        )


        ax.hist(
            df["valor"],
            bins=30,
            edgecolor="black"
        )


        ax.set_title(
            "Distribuição dos valores",
            fontsize=14,
            fontweight="bold"
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



    # Boxplot
    with col2:

        fig, ax = plt.subplots(
            figsize=(7,4)
        )


        ax.boxplot(
            df["valor"],
            vert=False,
            showmeans=True,
            patch_artist=True
        )


        ax.set_title(
            "Diagrama de caixa com média",
            fontsize=14,
            fontweight="bold"
        )


        ax.set_xlabel(
            "Valor"
        )


        ax.grid(
            alpha=0.3
        )


        fig.tight_layout()


        st.pyplot(fig)



# ======================================
# ABA 3 - SAZONALIDADE
# ======================================

with aba3:

    st.subheader(
        "Mapa de calor temporal"
    )


    heatmap_data = pd.pivot_table(
        df,
        values="valor",
        index="ano",
        columns="mes",
        aggfunc="mean"
    )


    fig, ax = plt.subplots(
        figsize=(12,6)
    )


    imagem = ax.imshow(
        heatmap_data,
        aspect="auto",
        cmap="viridis"
    )


    fig.colorbar(
        imagem,
        ax=ax,
        label="Valor médio"
    )


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


    ax.set_yticks(
        range(len(heatmap_data.index))
    )


    ax.set_yticklabels(
        heatmap_data.index
    )


    ax.set_xlabel(
        "Mês"
    )


    ax.set_ylabel(
        "Ano"
    )


    ax.set_title(
        "Mapa de calor do IBCR-PE",
        fontsize=16,
        fontweight="bold"
    )


    fig.tight_layout()


    st.pyplot(fig)



# ======================================
# ABA 4 - ANÁLISE ANUAL
# ======================================

with aba4:

    st.subheader(
        "Média anual do IBCR-PE"
    )


    media_ano = df.groupby(
        "ano"
    )["valor"].mean()


    fig, ax = plt.subplots(
        figsize=(10,5)
    )


    ax.barh(
        media_ano.index.astype(str),
        media_ano.values,
        edgecolor="black"
    )


    ax.set_title(
        "Valor médio por ano",
        fontsize=16,
        fontweight="bold"
    )


    ax.set_xlabel(
        "Valor médio"
    )


    ax.set_ylabel(
        "Ano"
    )


    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.3
    )


    fig.tight_layout()


    st.pyplot(fig)
