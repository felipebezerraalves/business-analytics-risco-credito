
# Análise de Carteira de Crédito e Risco de Inadimplência

Projeto de análise de dados financeiros utilizando SQL e Python para explorar uma amostra histórica de 1.000 empréstimos da LendingClub.

O objetivo foi identificar padrões associados aos contratos baixados (Charged Off), analisar classificações de risco e entender como características dos empréstimos se relacionam com esses contratos.

## Ferramentas utilizadas

- SQL e SQLite
- DBeaver
- Python e pandas
- Matplotlib e Plotly
- Streamlit

## Principais análises

- Indicadores gerais da carteira de crédito.
- Distribuição por classificação de risco.
- Relação entre score FICO e contratos baixados.
- Comparação entre empréstimos de 36 e 60 meses.
- Concentração financeira dos contratos baixados.
- Construção de gráficos e dashboard interativo.

## Principais resultados

- Foram analisados 1.000 empréstimos, totalizando US$ 14.524.250 em valores originalmente concedidos.
- 19,7% dos contratos foram classificados como Charged Off.
- Os empréstimos de 60 meses apresentaram maior proporção de contratos baixados.
- As classificações C, D e E concentraram aproximadamente 75% do valor originalmente concedido aos contratos baixados.
- As faixas FICO mais elevadas apresentaram menores proporções de contratos baixados na amostra.

## Uso de Inteligência Artificial

Durante o desenvolvimento deste projeto, utilizei inteligência artificial como apoio em algumas etapas, principalmente na construção dos gráficos, na elaboração dos scripts Python e na conferência dos resultados obtidos com SQL.

A ferramenta também me ajudou a entender melhor algumas análises, revisar códigos e encontrar formas mais claras de apresentar os dados.

Ao longo do processo, procurei comparar os resultados entre SQL e Python, entender os indicadores e conferir se as informações apresentadas faziam sentido.

Para mim, a IA foi uma ferramenta de apoio ao aprendizado e ao desenvolvimento do projeto, enquanto a interpretação dos resultados continuou sendo uma parte importante do trabalho.

## Arquivos do projeto

- `consultas_sql/`: scripts SQL utilizados nas análises.
- `analise_python/`: scripts Python para análise, gráficos, dashboard e relatório.
- `graficos/`: visualizações dos indicadores.
- `apresentacao_executiva/`: relatório executivo em PDF.

## Base de dados

Foi utilizada uma amostra histórica de empréstimos da LendingClub, disponível no repositório:

https://github.com/BrielleCS/LendingClub-Loan-Portfolio-Analysis

O arquivo utilizado foi `accepted_loans_sample.csv`.

Por questões de organização e para evitar a redistribuição não verificada dos dados, o CSV e o banco SQLite não foram incluídos neste repositório.

Para executar as análises localmente, é necessário obter a amostra na fonte indicada, salvá-la em `dados_originais/accepted_loans_sample.csv` e preparar o banco SQLite utilizado pelos scripts SQL.

## Relatório executivo

O projeto também conta com um relatório executivo em PDF, reunindo os indicadores, as principais análises e as conclusões.

[Visualizar relatório executivo](apresentacao_executiva/relatorio_executivo_risco_credito.pdf)

## Observações

Os resultados representam apenas a amostra analisada e não devem ser generalizados para toda a carteira da LendingClub.

O status Charged Off não representa necessariamente o valor de perda financeira líquida.

---

**Autor:** Felipe Bezerra Alves
