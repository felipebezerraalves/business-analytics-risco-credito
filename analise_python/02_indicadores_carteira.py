
# PROJETO 04
# 02 | INDICADORES GERAIS DA CARTEIRA

import pandas as pd
from pathlib import Path

# 1. Localizar e carregar o CSV
pasta_projeto = Path(__file__).resolve().parent.parent
arquivo_csv = pasta_projeto / "dados_originais" / "accepted_loans_sample.csv"

df = pd.read_csv(arquivo_csv)

# 2. Calcular os indicadores gerais
print("\n1. INDICADORES GERAIS")

print("Total de emprestimos:", len(df))
print("Valor total concedido:", round(df["loan_amnt"].sum(), 2))
print("Valor medio:", round(df["loan_amnt"].mean(), 2))
print("Menor emprestimo:", df["loan_amnt"].min())
print("Maior emprestimo:", df["loan_amnt"].max())
print("Taxa media de juros:", round(df["int_rate"].mean(), 2))

# 3. Agrupar os valores por situacao
print("\n2. INDICADORES POR SITUACAO")

indicadores_status = df.groupby("loan_status").agg(
    quantidade_emprestimos=("id", "count"),
    valor_total_concedido=("loan_amnt", "sum"),
    valor_medio_emprestimo=("loan_amnt", "mean")
)

print(indicadores_status.round(2))

# 4. Calcular o percentual de contratos baixados
print("\n3. PERCENTUAL DE CONTRATOS BAIXADOS")

total_contratos = len(df)
contratos_baixados = (df["loan_status"] == "Charged Off").sum()

percentual_baixados = contratos_baixados / total_contratos * 100

print("Contratos baixados:", contratos_baixados)
print("Percentual de contratos baixados:", round(percentual_baixados, 2))
