
# PROJETO 04
# 09 | RELATÓRIO EXECUTIVO DE RISCO DE CRÉDITO

from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)


# 1. LOCALIZAR OS ARQUIVOS DO PROJETO

pasta_projeto = Path(__file__).resolve().parent.parent

arquivo_csv = (
    pasta_projeto
    / "dados_originais"
    / "accepted_loans_sample.csv"
)

pasta_graficos = pasta_projeto / "graficos"

pasta_relatorio = (
    pasta_projeto / "apresentacao_executiva"
)

pasta_relatorio.mkdir(exist_ok=True)

arquivo_pdf = (
    pasta_relatorio
    / "relatorio_executivo_risco_credito.pdf"
)


# 2. CONFIGURAR FONTES COM ACENTUAÇÃO

pasta_fontes = Path("C:/Windows/Fonts")

pdfmetrics.registerFont(
    TTFont(
        "Arial",
        str(pasta_fontes / "arial.ttf")
    )
)

pdfmetrics.registerFont(
    TTFont(
        "Arial-Bold",
        str(pasta_fontes / "arialbd.ttf")
    )
)

pdfmetrics.registerFontFamily(
    "Arial",
    normal="Arial",
    bold="Arial-Bold"
)


# 3. CARREGAR E ANALISAR OS DADOS

df = pd.read_csv(arquivo_csv)

total_emprestimos = len(df)

valor_concedido = df["loan_amnt"].sum()

emprestimo_medio = df["loan_amnt"].mean()

juros_medios = df["int_rate"].mean()

df["contrato_baixado"] = (
    df["loan_status"] == "Charged Off"
).astype(int)

contratos_baixados = int(
    df["contrato_baixado"].sum()
)

percentual_baixados = (
    contratos_baixados
    / total_emprestimos
    * 100
)

valor_concedido_baixados = df.loc[
    df["contrato_baixado"] == 1,
    "loan_amnt"
].sum()

percentual_valor_baixados = (
    valor_concedido_baixados
    / valor_concedido
    * 100
)


# 4. FUNÇÕES PARA FORMATAR NÚMEROS

def moeda(valor):
    numero = f"{valor:,.2f}"
    numero = numero.replace(",", "X")
    numero = numero.replace(".", ",")
    numero = numero.replace("X", ".")
    return f"US$ {numero}"


def percentual(valor):
    return f"{valor:.2f}".replace(".", ",") + "%"


def inteiro(valor):
    return f"{valor:,}".replace(",", ".")


# 5. CONFIGURAR O DOCUMENTO PDF

documento = SimpleDocTemplate(
    str(arquivo_pdf),
    pagesize=A4,
    rightMargin=48,
    leftMargin=48,
    topMargin=48,
    bottomMargin=48
)

estilos = getSampleStyleSheet()

azul_escuro = colors.HexColor("#17324D")
cinza_claro = colors.HexColor("#D7DEE5")


# Estilo do título principal

estilos.add(ParagraphStyle(
    name="TituloRelatorio",
    parent=estilos["Title"],
    fontName="Arial-Bold",
    fontSize=22,
    leading=28,
    textColor=azul_escuro,
    spaceAfter=18,
    alignment=TA_CENTER
))


# Estilo dos subtítulos

estilos.add(ParagraphStyle(
    name="SubtituloRelatorio",
    parent=estilos["Heading2"],
    fontName="Arial-Bold",
    fontSize=14,
    leading=18,
    textColor=azul_escuro,
    spaceAfter=12
))


# Estilo dos parágrafos

estilos.add(ParagraphStyle(
    name="TextoRelatorio",
    parent=estilos["BodyText"],
    fontName="Arial",
    fontSize=10,
    leading=16,
    spaceAfter=10,
    alignment=TA_LEFT
))


# Estilo de textos centralizados

estilos.add(ParagraphStyle(
    name="TextoCentralizado",
    parent=estilos["BodyText"],
    fontName="Arial",
    fontSize=11,
    leading=18,
    alignment=TA_CENTER
))


# 6. FUNÇÕES PARA MONTAR O RELATÓRIO

elementos = []


def titulo(conteudo):
    elementos.append(
        Paragraph(
            conteudo,
            estilos["TituloRelatorio"]
        )
    )


def subtitulo(conteudo):
    elementos.append(
        Paragraph(
            conteudo,
            estilos["SubtituloRelatorio"]
        )
    )


def texto(conteudo):
    elementos.append(
        Paragraph(
            conteudo,
            estilos["TextoRelatorio"]
        )
    )


def adicionar_grafico(nome_arquivo, largura=390):

    caminho = pasta_graficos / nome_arquivo

    if caminho.exists():

        imagem = ImageReader(str(caminho))

        largura_original, altura_original = (
            imagem.getSize()
        )

        altura = (
            largura
            * altura_original
            / largura_original
        )

        elementos.append(
            Image(
                str(caminho),
                width=largura,
                height=altura
            )
        )

    else:

        texto(
            f"Gráfico não encontrado: {nome_arquivo}"
        )


def adicionar_tabela(dados, larguras):

    tabela = Table(
        dados,
        colWidths=larguras,
        repeatRows=1
    )

    tabela.setStyle(TableStyle([

        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            azul_escuro
        ),

        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white
        ),

        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "Arial-Bold"
        ),

        (
            "FONTNAME",
            (0, 1),
            (-1, -1),
            "Arial"
        ),

        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            9
        ),

        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            10
        ),

        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            10
        ),

        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.3,
            cinza_claro
        ),

        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        )

    ]))

    elementos.append(tabela)


# ============================================
# PÁGINA 1 | CAPA
# ============================================

elementos.append(Spacer(1, 120))

titulo(
    "Análise de Carteira de Crédito "
    "e Risco de Inadimplência"
)

elementos.append(Spacer(1, 18))

elementos.append(
    Paragraph(
        "Estudo exploratório de empréstimos "
        "da LendingClub",
        estilos["TextoCentralizado"]
    )
)

elementos.append(Spacer(1, 50))

elementos.append(
    Paragraph(
        "SQL | Python | pandas | Matplotlib "
        "| Plotly | Streamlit",
        estilos["TextoCentralizado"]
    )
)

elementos.append(Spacer(1, 100))

elementos.append(
    Paragraph(
        "Felipe Bezerra Alves | Projeto de Portfólio",
        estilos["TextoCentralizado"]
    )
)

elementos.append(PageBreak())


# ============================================
# PÁGINA 2 | OBJETIVO E METODOLOGIA
# ============================================

titulo("Objetivo e Metodologia")

subtitulo("Objetivo da análise")

texto(
    "Analisar o perfil de uma amostra histórica de "
    "empréstimos e identificar padrões associados "
    "a contratos classificados como Charged Off."
)

subtitulo("Base de dados")

texto(
    "A análise utiliza 1.000 registros de empréstimos "
    "da LendingClub, contendo informações sobre valores "
    "concedidos, taxas de juros, prazos, score FICO, "
    "classificação de risco e situação dos contratos."
)

subtitulo("Metodologia")

texto(
    "Os dados foram explorados utilizando SQL e SQLite. "
    "As análises foram reproduzidas em Python com pandas. "
    "Os resultados foram visualizados com Matplotlib e "
    "Plotly e reunidos em um dashboard interativo "
    "desenvolvido com Streamlit."
)

subtitulo("Limitações da análise")

texto(
    "Os resultados representam apenas a amostra estudada "
    "e não necessariamente toda a carteira da instituição. "
    "O status Charged Off indica baixa como perda, "
    "mas o valor originalmente concedido aos contratos "
    "baixados não equivale ao prejuízo financeiro líquido."
)

elementos.append(PageBreak())


# ============================================
# PÁGINA 3 | INDICADORES GERAIS
# ============================================

titulo("Indicadores Gerais da Carteira")

dados_indicadores = [

    ["Indicador", "Resultado"],

    [
        "Quantidade de empréstimos",
        inteiro(total_emprestimos)
    ],

    [
        "Valor total concedido",
        moeda(valor_concedido)
    ],

    [
        "Valor médio por empréstimo",
        moeda(emprestimo_medio)
    ],

    [
        "Taxa média de juros",
        percentual(juros_medios)
    ],

    [
        "Contratos Charged Off",
        inteiro(contratos_baixados)
    ],

    [
        "Percentual Charged Off",
        percentual(percentual_baixados)
    ],

    [
        "Valor concedido aos contratos baixados",
        moeda(valor_concedido_baixados)
    ],

    [
        "Participação financeira dos baixados",
        percentual(percentual_valor_baixados)
    ]

]

adicionar_tabela(
    dados_indicadores,
    [275, 215]
)

elementos.append(Spacer(1, 25))

texto(
    "Os contratos classificados como Charged Off "
    "representam 19,70% das operações analisadas "
    "e 21,48% do valor originalmente concedido "
    "na amostra."
)

elementos.append(PageBreak())


# ============================================
# PÁGINA 4 | RESULTADOS DE RISCO
# ============================================

titulo("Principais Resultados de Risco")

subtitulo("Classificação de risco")

texto(
    "A proporção de contratos Charged Off cresce "
    "entre as classificações A e E, passando "
    "de 4,76% para 39,53%."
)

adicionar_grafico(
    "01_contratos_baixados_por_grade.png",
    largura=390
)

elementos.append(Spacer(1, 12))

subtitulo("Prazo do empréstimo")

texto(
    "Empréstimos de 60 meses apresentam 34,36% "
    "de contratos baixados, contra 14,57% "
    "nos contratos de 36 meses."
)

elementos.append(PageBreak())


# ============================================
# PÁGINA 5 | CONCLUSÕES
# ============================================

titulo("Conclusões e Recomendações")

subtitulo("Principais resultados")

texto(
    "A amostra apresenta associações entre "
    "classificação de risco, prazo de pagamento "
    "e score FICO com a frequência de contratos "
    "baixados como perda."
)

texto(
    "As classificações C, D e E concentram "
    "aproximadamente 75% do valor originalmente "
    "concedido aos contratos Charged Off."
)

subtitulo("Recomendações")

texto(
    "Monitorar conjuntamente a proporção de "
    "contratos baixados e a concentração financeira, "
    "considerando classificação de risco, prazo "
    "e score FICO."
)

texto(
    "Ampliar a base de dados e considerar diferentes "
    "safras de concessão antes de propor alterações "
    "nas políticas de crédito."
)

subtitulo("Observações metodológicas")

texto(
    "Os resultados não estabelecem causalidade, "
    "não representam estimativas de perda esperada "
    "e não devem ser generalizados para toda "
    "a carteira da LendingClub."
)


# 7. GERAR O RELATÓRIO

documento.build(elementos)

print("\nRelatório gerado com sucesso!")
print("Arquivo salvo em:")
print(arquivo_pdf)
