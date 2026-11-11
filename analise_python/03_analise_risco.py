
# PROJETO 04
# 03 | ANALISE DE RISCO DE CREDITO

import pandas as pd
from pathlib import Path

# 1. Carregar a base
pasta_projeto = Path(__file__).resolve().parent.parent
arquivo_csv = pasta_projeto / "dados_originais" / "accepted_loans_sample.csv"

df = pd.read_csv(arquivo_csv)

# 2. Criar indicador de contratos baixados
df["contrato_baixado"] = (
    df["loan_status"] == "Charged Off"
).astype(int)

# 3. Calcular indicadores por classificacao de risco
analise_risco = df.groupby("grade").agg(
    total_emprestimos=("id", "count"),
    contratos_baixados=("contrato_baixado", "sum"),
    valor_concedido=("loan_amnt", "sum"),
    juros_medios=("int_rate", "mean")
)

# 4. Calcular percentual de contratos baixados
analise_risco["percentual_baixados"] = (
    analise_risco["contratos_baixados"]
    / analise_risco["total_emprestimos"]
    * 100
)

# 5. Apresentar os resultados
print("\nANALISE DE RISCO POR CLASSIFICACAO")
print(analise_risco.round(2))
