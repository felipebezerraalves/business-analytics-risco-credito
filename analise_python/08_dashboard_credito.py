
# PROJETO 04
# 08 | DASHBOARD EXECUTIVO DE RISCO DE CREDITO
# Base: LendingClub - amostra historica de 1.000 emprestimos

import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path


# 1. CONFIGURAR A PAGINA

st.set_page_config(
    page_title="Dashboard de Risco de Credito",
    page_icon="📊",
    layout="wide"
)


# 2. LOCALIZAR E CARREGAR OS DADOS

pasta_projeto = Path(__file__).resolve().parent.parent
arquivo_csv = (
    pasta_projeto
    / "dados_originais"
    / "accepted_loans_sample.csv"
)


@st.cache_data
def carregar_dados():
    dados = pd.read_csv(arquivo_csv)

    dados["contrato_baixado"] = (
        dados["loan_status"] == "Charged Off"
    ).astype(int)

    return dados


df = carregar_dados()


# 3. APRESENTACAO DO DASHBOARD

st.title("Dashboard de Risco de Credito")

st.write(
    "Analise exploratoria de uma amostra historica "
    "de emprestimos da LendingClub."
)

st.caption(
    "Valores financeiros em dolares americanos (US$). "
    "Os indicadores representam apenas os contratos "
    "selecionados nos filtros."
)


# 4. FILTROS INTERATIVOS

st.sidebar.header("Filtros da carteira")

classificacoes = sorted(
    df["grade"].dropna().unique()
)

prazos = sorted(
    df["term"].dropna().unique()
)

grades_selecionadas = st.sidebar.multiselect(
    "Classificacao de risco",
    options=classificacoes,
    default=list(classificacoes)
)

prazos_selecionados = st.sidebar.multiselect(
    "Prazo do emprestimo",
    options=prazos,
    default=list(prazos)
)


# 5. APLICAR OS FILTROS

df_filtrado = df[
    df["grade"].isin(grades_selecionadas)
    & df["term"].isin(prazos_selecionados)
].copy()

if df_filtrado.empty:
    st.warning(
        "Nenhum emprestimo encontrado para os filtros."
    )
    st.stop()


# 6. INDICADORES GERAIS

total_emprestimos = len(df_filtrado)

valor_concedido = df_filtrado["loan_amnt"].sum()

juros_medios = df_filtrado["int_rate"].mean()

contratos_baixados = (
    df_filtrado["contrato_baixado"].sum()
)

percentual_baixados = (
    contratos_baixados
    / total_emprestimos
    * 100
)

valor_concedido_baixados = df_filtrado.loc[
    df_filtrado["contrato_baixado"] == 1,
    "loan_amnt"
].sum()


st.subheader("Indicadores gerais")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total de emprestimos",
    f"{total_emprestimos:,}"
)

col2.metric(
    "Valor concedido",
    f"US$ {valor_concedido:,.2f}"
)

col3.metric(
    "Juros medios",
    f"{juros_medios:.2f}%"
)

col4.metric(
    "Contratos Charged Off",
    f"{percentual_baixados:.2f}%"
)

st.metric(
    "Valor concedido a contratos Charged Off",
    f"US$ {valor_concedido_baixados:,.2f}"
)

st.caption(
    "O valor concedido a contratos Charged Off "
    "nao corresponde a perda financeira liquida."
)

st.divider()


# 7. ANALISE POR CLASSIFICACAO DE RISCO

st.subheader("Risco por classificacao")

analise_grade = df_filtrado.groupby(
    "grade", as_index=False
).agg(
    total_emprestimos=("id", "count"),
    contratos_baixados=("contrato_baixado", "sum")
)

analise_grade["percentual_baixados"] = (
    analise_grade["contratos_baixados"]
    / analise_grade["total_emprestimos"]
    * 100
)

fig_grade = px.bar(
    analise_grade,
    x="grade",
    y="percentual_baixados",
    text="percentual_baixados",
    hover_data=[
        "total_emprestimos",
        "contratos_baixados"
    ],
    labels={
        "grade": "Classificacao de risco",
        "percentual_baixados": "Contratos baixados (%)",
        "total_emprestimos": "Total de contratos",
        "contratos_baixados": "Contratos baixados"
    },
    title="Percentual de contratos baixados por grade"
)

fig_grade.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_grade.update_layout(
    yaxis_range=[
        0,
        max(
            5,
            analise_grade["percentual_baixados"].max()
            * 1.2
        )
    ]
)

st.plotly_chart(
    fig_grade,
    use_container_width=True
)

st.caption(
    "Atencao: as classificacoes F e G apresentam "
    "poucos contratos na amostra completa. "
    "Considere sempre o tamanho de cada grupo."
)

st.divider()


# 8. CONCENTRACAO FINANCEIRA

st.subheader("Concentracao financeira do risco")

df_baixados = df_filtrado[
    df_filtrado["contrato_baixado"] == 1
].copy()

if not df_baixados.empty:

    exposicao = df_baixados.groupby(
        "grade", as_index=False
    ).agg(
        valor_concedido_baixados=("loan_amnt", "sum"),
        quantidade_baixados=("id", "count")
    )

    total_valor_baixados = (
        exposicao["valor_concedido_baixados"].sum()
    )

    exposicao["percentual_concentracao"] = (
        exposicao["valor_concedido_baixados"]
        / total_valor_baixados
        * 100
    )

    exposicao = exposicao.sort_values(
        "valor_concedido_baixados",
        ascending=False
    )

    fig_exposicao = px.bar(
        exposicao,
        x="grade",
        y="valor_concedido_baixados",
        text="valor_concedido_baixados",
        hover_data=[
            "percentual_concentracao",
            "quantidade_baixados"
        ],
        labels={
            "grade": "Classificacao de risco",
            "valor_concedido_baixados":
                "Valor originalmente concedido (US$)",
            "percentual_concentracao":
                "Participacao no total (%)",
            "quantidade_baixados":
                "Contratos baixados"
        },
        title="Valor concedido a contratos Charged Off"
    )

    fig_exposicao.update_traces(
        texttemplate="US$ %{text:,.0f}",
        textposition="outside"
    )

    fig_exposicao.update_layout(
        yaxis_range=[
            0,
            exposicao["valor_concedido_baixados"].max()
            * 1.2
        ]
    )

    st.plotly_chart(
        fig_exposicao,
        use_container_width=True
    )

    st.write(
        "Participacao de cada classificacao "
        "no valor concedido aos contratos baixados:"
    )

    st.dataframe(
        exposicao.round(2),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(
        "Nenhum contrato Charged Off encontrado "
        "nos filtros selecionados."
    )

st.divider()


# 9. ANALISE POR PRAZO

st.subheader("Risco por prazo do emprestimo")

analise_prazo = df_filtrado.groupby(
    "term", as_index=False
).agg(
    total_emprestimos=("id", "count"),
    contratos_baixados=("contrato_baixado", "sum")
)

analise_prazo["percentual_baixados"] = (
    analise_prazo["contratos_baixados"]
    / analise_prazo["total_emprestimos"]
    * 100
)

fig_prazo = px.bar(
    analise_prazo,
    x="term",
    y="percentual_baixados",
    text="percentual_baixados",
    hover_data=[
        "total_emprestimos",
        "contratos_baixados"
    ],
    labels={
        "term": "Prazo do emprestimo",
        "percentual_baixados": "Contratos baixados (%)",
        "total_emprestimos": "Total de contratos",
        "contratos_baixados": "Contratos baixados"
    },
    title="Percentual de contratos baixados por prazo"
)

fig_prazo.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_prazo,
    use_container_width=True
)

st.divider()


# 10. ANALISE POR SCORE FICO

st.subheader("Risco por faixa de score FICO")

df_fico = df_filtrado.dropna(
    subset=["fico_range_low"]
).copy()

df_fico["faixa_fico"] = pd.cut(
    df_fico["fico_range_low"],
    bins=[0, 650, 700, 750, float("inf")],
    labels=[
        "Abaixo de 650",
        "650 a 699",
        "700 a 749",
        "750 ou mais"
    ],
    right=False
)

analise_fico = df_fico.groupby(
    "faixa_fico",
    observed=True
).agg(
    total_emprestimos=("id", "count"),
    contratos_baixados=("contrato_baixado", "sum")
).reset_index()

if not analise_fico.empty:

    analise_fico["percentual_baixados"] = (
        analise_fico["contratos_baixados"]
        / analise_fico["total_emprestimos"]
        * 100
    )

    fig_fico = px.bar(
        analise_fico,
        x="faixa_fico",
        y="percentual_baixados",
        text="percentual_baixados",
        hover_data=[
            "total_emprestimos",
            "contratos_baixados"
        ],
        labels={
            "faixa_fico": "Faixa de score FICO",
            "percentual_baixados":
                "Contratos baixados (%)",
            "total_emprestimos": "Total de contratos",
            "contratos_baixados": "Contratos baixados"
        },
        title="Percentual de contratos baixados por FICO"
    )

    fig_fico.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig_fico,
        use_container_width=True
    )

else:
    st.info(
        "Nao ha registros com score FICO "
        "para os filtros selecionados."
    )

st.divider()


# 11. TABELA DOS EMPRESTIMOS

st.subheader("Dados da carteira")

st.dataframe(
    df_filtrado[
        [
            "id",
            "loan_amnt",
            "grade",
            "term",
            "int_rate",
            "fico_range_low",
            "loan_status"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# 12. OBSERVACOES METODOLOGICAS

st.subheader("Observacoes metodologicas")

st.info(
    "Esta analise utiliza uma amostra historica "
    "de 1.000 emprestimos da LendingClub. "
    "Os resultados nao representam necessariamente "
    "toda a carteira da instituicao."
)

st.warning(
    "O status Charged Off indica baixa como perda. "
    "O valor originalmente concedido a esses contratos "
    "nao equivale ao prejuizo liquido efetivo. "
    "As analises nao estabelecem relacoes causais."
)

st.caption(
    "Projeto de portfolio | SQL, Python, pandas, "
    "Plotly e Streamlit."
)
