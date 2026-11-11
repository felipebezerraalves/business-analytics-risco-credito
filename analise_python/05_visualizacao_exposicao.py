
# PROJETO 04
# 05 | VISUALIZACAO DA EXPOSICAO FINANCEIRA

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Localizar a base e a pasta de graficos
pasta_projeto = Path(__file__).resolve().parent.parent
arquivo_csv = pasta_projeto / "dados_originais" / "accepted_loans_sample.csv"
pasta_graficos = pasta_projeto / "graficos"

pasta_graficos.mkdir(exist_ok=True)

# 2. Carregar os dados
df = pd.read_csv(arquivo_csv)

# 3. Selecionar somente contratos baixados
contratos_baixados = df[
    df["loan_status"] == "Charged Off"
]

# 4. Somar os valores concedidos por grade
exposicao = (
    contratos_baixados.groupby("grade")["loan_amnt"]
    .sum()
    .sort_values(ascending=False)
)

# 5. Criar o grafico
plt.figure(figsize=(10, 6))

plt.bar(
    exposicao.index,
    exposicao.values
)

plt.title("Valor concedido a contratos Charged Off por grade")
plt.xlabel("Classificacao de risco")
plt.ylabel("Valor originalmente concedido (US$)")

# 6. Mostrar valores acima das barras
for i, valor in enumerate(exposicao.values):
    plt.text(
        i,
        valor + 15000,
        f"US$ {valor:,.0f}",
        ha="center",
        fontsize=9
    )

# 7. Ajustar e salvar
plt.ylim(0, exposicao.max() * 1.15)
plt.tight_layout()

arquivo_grafico = (
    pasta_graficos / "02_exposicao_financeira_por_grade.png"
)

plt.savefig(arquivo_grafico, dpi=300)
plt.show()

print("\nGrafico salvo em:")
print(arquivo_grafico)
