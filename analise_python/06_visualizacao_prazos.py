
# PROJETO 04
# 06 | VISUALIZACAO DO RISCO POR PRAZO

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

# 3. Identificar contratos baixados
df["contrato_baixado"] = (
    df["loan_status"] == "Charged Off"
).astype(int)

# 4. Calcular os indicadores por prazo
analise_prazo = df.groupby("term").agg(
    total_emprestimos=("id", "count"),
    contratos_baixados=("contrato_baixado", "sum")
)

analise_prazo["percentual_baixados"] = (
    analise_prazo["contratos_baixados"]
    / analise_prazo["total_emprestimos"]
    * 100
)

analise_prazo = analise_prazo.sort_index()

# 5. Mostrar os resultados
print("\nANALISE DE RISCO POR PRAZO")
print(analise_prazo.round(2))

# 6. Criar o grafico
plt.figure(figsize=(9, 6))

plt.bar(
    analise_prazo.index,
    analise_prazo["percentual_baixados"]
)

plt.title("Contratos baixados por prazo do emprestimo")
plt.xlabel("Prazo do emprestimo")
plt.ylabel("Contratos baixados (%)")

# 7. Adicionar percentuais
for i, percentual in enumerate(analise_prazo["percentual_baixados"]):
    plt.text(
        i,
        percentual + 0.5,
        f"{percentual:.2f}%",
        ha="center"
    )

# 8. Ajustar e salvar
plt.ylim(0, 40)
plt.tight_layout()

arquivo_grafico = (
    pasta_graficos / "03_contratos_baixados_por_prazo.png"
)

plt.savefig(arquivo_grafico, dpi=300)
plt.show()

print("\nGrafico salvo em:")
print(arquivo_grafico)
