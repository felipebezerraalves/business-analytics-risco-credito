
# PROJETO 04
# 07 | VISUALIZACAO DO RISCO POR SCORE FICO

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Localizar os arquivos
pasta_projeto = Path(__file__).resolve().parent.parent
arquivo_csv = pasta_projeto / "dados_originais" / "accepted_loans_sample.csv"
pasta_graficos = pasta_projeto / "graficos"

pasta_graficos.mkdir(exist_ok=True)

# 2. Carregar os dados
df = pd.read_csv(arquivo_csv)

# 3. Remover apenas registros sem score FICO
df = df.dropna(subset=["fico_range_low"]).copy()

# 4. Identificar contratos baixados
df["contrato_baixado"] = (
    df["loan_status"] == "Charged Off"
).astype(int)

# 5. Criar faixas de FICO
df["faixa_fico"] = pd.cut(
    df["fico_range_low"],
    bins=[0, 650, 700, 750, float("inf")],
    labels=[
        "Abaixo de 650",
        "650 a 699",
        "700 a 749",
        "750 ou mais"
    ],
    right=False
)

# 6. Calcular indicadores por faixa
analise_fico = df.groupby(
    "faixa_fico",
    observed=True
).agg(
    total_emprestimos=("id", "count"),
    contratos_baixados=("contrato_baixado", "sum")
)

analise_fico["percentual_baixados"] = (
    analise_fico["contratos_baixados"]
    / analise_fico["total_emprestimos"]
    * 100
)

# 7. Mostrar resultados
print("\nANALISE DE RISCO POR SCORE FICO")
print(analise_fico.round(2))

# 8. Criar grafico
plt.figure(figsize=(10, 6))

plt.bar(
    analise_fico.index.astype(str),
    analise_fico["percentual_baixados"]
)

plt.title("Contratos baixados por faixa de score FICO")
plt.xlabel("Faixa de score FICO")
plt.ylabel("Contratos baixados (%)")

# 9. Adicionar percentuais
for i, percentual in enumerate(analise_fico["percentual_baixados"]):
    plt.text(
        i,
        percentual + 0.4,
        f"{percentual:.2f}%",
        ha="center"
    )

# 10. Salvar e exibir
plt.ylim(0, 30)
plt.tight_layout()

arquivo_grafico = (
    pasta_graficos / "04_contratos_baixados_por_fico.png"
)

plt.savefig(arquivo_grafico, dpi=300)
plt.show()

print("\nGrafico salvo em:")
print(arquivo_grafico)
