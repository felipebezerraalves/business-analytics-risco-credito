
# PROJETO 04
# 04 | VISUALIZACAO DO RISCO DE CREDITO

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Definir os caminhos do projeto
pasta_projeto = Path(__file__).resolve().parent.parent
arquivo_csv = pasta_projeto / "dados_originais" / "accepted_loans_sample.csv"
pasta_graficos = pasta_projeto / "graficos"

# 2. Garantir que a pasta de graficos existe
pasta_graficos.mkdir(exist_ok=True)

# 3. Carregar os dados
df = pd.read_csv(arquivo_csv)

# 4. Identificar os contratos baixados
df["contrato_baixado"] = (
    df["loan_status"] == "Charged Off"
).astype(int)

# 5. Calcular o percentual por classificacao
analise_risco = df.groupby("grade").agg(
    total_emprestimos=("id", "count"),
    contratos_baixados=("contrato_baixado", "sum")
)

analise_risco["percentual_baixados"] = (
    analise_risco["contratos_baixados"]
    / analise_risco["total_emprestimos"]
    * 100
)

# 6. Criar o grafico de barras
plt.figure(figsize=(10, 6))

plt.bar(
    analise_risco.index,
    analise_risco["percentual_baixados"]
)

plt.title("Contratos baixados por classificacao de risco")
plt.xlabel("Classificacao de risco")
plt.ylabel("Contratos baixados (%)")

# 7. Exibir os percentuais acima das barras
for i, percentual in enumerate(analise_risco["percentual_baixados"]):
    plt.text(
        i,
        percentual + 0.5,
        f"{percentual:.2f}%",
        ha="center"
    )

# 8. Ajustar e salvar o grafico
plt.ylim(0, 45)
plt.tight_layout()

arquivo_grafico = pasta_graficos / "01_contratos_baixados_por_grade.png"

plt.savefig(arquivo_grafico, dpi=300)
plt.show()

print("\nGrafico salvo em:")
print(arquivo_grafico)
