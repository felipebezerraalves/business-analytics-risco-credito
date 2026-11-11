
# PROJETO 04
# 01 | EXPLORACAO INICIAL DOS DADOS

import pandas as pd
from pathlib import Path

# 1. Localizar o arquivo CSV
pasta_projeto = Path(__file__).resolve().parent.parent
arquivo_csv = pasta_projeto / "dados_originais" / "accepted_loans_sample.csv"

# 2. Carregar os dados
df = pd.read_csv(arquivo_csv)

# 3. Verificar a quantidade de linhas e colunas
print("\n1. DIMENSOES DA BASE")
print(df.shape)

# 4. Visualizar os primeiros registros
print("\n2. PRIMEIROS CINCO REGISTROS")
print(df.head())

# 5. Consultar os tipos de dados
print("\n3. TIPOS DE DADOS")
print(df.dtypes)

# 6. Verificar valores ausentes
print("\n4. VALORES AUSENTES")
print(df.isnull().sum())

# 7. Consultar os status dos emprestimos
print("\n5. SITUACAO DOS EMPRESTIMOS")
print(df["loan_status"].value_counts())




