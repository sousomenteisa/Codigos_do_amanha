
#DESAFIO — Aula 4: Pandas com dados do Boticário
#================================================

#Você é analista de uma loja e precisa responder perguntas sobre o catálogo
#de produtos usando o arquivo `boticario_products.csv`.

#Use apenas o que vimos na Aula_4.py:
# - pd.read_csv, .head(), .shape, .columns, .dtypes, .iloc
#- Seleção de colunas: df[["col1", "col2"]]
#- Filtros com condições: df[df["col"] == valor] e operador &
#- Novas colunas: cálculos, .map() e pd.cut()
#- .sort_values(), .value_counts(), .groupby()
#- .rename() e .drop_duplicates()

#Regras:
#1. Cada tarefa deve ter seu próprio bloco de código.
#2. Use print() com um título claro antes de cada resposta.
#3. Não altere o arquivo CSV original.
#4. Bônus: tente resolver sem olhar a Aula_4.py — consulte só se travar!

#Pontuação sugerida: 10 pts (Tarefas 1–8) + 2 pts bônus (Desafio Final)
#"""

import pandas as pd

# ── Carregamento (já feito para você) ────────────────────────────────────────
df = pd.read_csv("boticario_products.csv")



# ═══════════════════════════════════════════════════════════════════════════
# TAREFA 1 — Conhecendo os dados (1 pt)
# ═══════════════════════════════════════════════════════════════════════════
# Imprima:
#   a) As 3 primeiras linhas do DataFrame
#   b) Quantas linhas e colunas existem
#   c) A lista com os nomes de TODAS as colunas
#   d) Os tipos de dados de cada coluna

# TODO: seu código aqui
print("\nTAREFA 1 - Conhecendo os dados\n")
print(df.head(3))
print(df.shape)
print(df.columns)
print(df.dtypes)






# ═══════════════════════════════════════════════════════════════════════════
# TAREFA 2 — Seleção e filtro (1,5 pts)
# ═══════════════════════════════════════════════════════════════════════════
# a) Crie um DataFrame `df_resumo` apenas com as colunas:
#    "name", "normalized_category", "regular_price", "promotional_price"
#    Mostre as 5 primeiras linhas.
#
# b) Filtre produtos da categoria "Corpo e Banho" que estão em promoção
#    (promotion_active == True). Imprima quantas linhas foram encontradas.

# TODO: seu código aqui

print("\n TAREFA 2 - Seleção e Filtro \n")

df_resumo = df[['name', 'normalized_category', 'regular_price', 'promotional_price', 'promotion_active']].head(20)
print(df_resumo)

filtro = df_resumo[(df_resumo['normalized_category'] == 'Corpo e Banho') & 
            (df_resumo['promotion_active'] == True)
            ]
print(df_resumo.head(5))
print(filtro.head(5))


# ═══════════════════════════════════════════════════════════════════════════
# TAREFA 3 — Criando colunas (1,5 pts)
# ═══════════════════════════════════════════════════════════════════════════
# a) Crie a coluna `economia_reais` = regular_price - promotional_price
#
# b) Crie a coluna `status_promo` usando .map():
#    True  → "Em promoção"
#    False → "Preço cheio"
#
# c) Filtre apenas produtos de "Perfumaria" e calcule a MÉDIA de economia_reais.
#    Imprima o valor com 2 casas decimais.

# TODO: seu código aqui

df['economia_reais'] = df['regular_price'] - df['promotional_price']

df['status_promo'] = df['promotion_active'].map({True: 'Em promoção', False: 'Preço cheio'})

df_perfumaria = df[df['normalized_category'] == 'Perfumaria']
media_economia = df_perfumaria['economia_reais'].mean()
print(f"\nMédia de economia em Perfumaria: R$ {media_economia:.2f}")

# ═══════════════════════════════════════════════════════════════════════════
# TAREFA 4 — Faixas de preço com pd.cut() (1 pt)
# ═══════════════════════════════════════════════════════════════════════════
# Crie a coluna `faixa_preco` dividindo promotional_price em:
#   Até R$ 50      → de 0 a 50
#   R$ 50-100      → de 50 a 100
#   R$ 100-200     → de 100 a 200
#   Acima de R$ 200 → acima de 200
#
# Conte quantos produtos estão na faixa "Até R$ 50" e imprima o resultado.

# TODO: seu código aqui

faixa_preco_bins = [0, 50, 100,200, float('inf')]
faixa_preco_labels = ['Até R$ 50', 'R$ 50-100', 'R$ 100-200', 'Acima de R$ 200']
df['faixa_preco'] = pd.cut(df['promotional_price'], bins=faixa_preco_bins, labels=faixa_preco_labels, right=False)
print(df['faixa_preco'].value_counts())

# ═══════════════════════════════════════════════════════════════════════════
# TAREFA 5 — Ordenação (1 pt)
# ═══════════════════════════════════════════════════════════════════════════
# Encontre os 3 produtos da categoria "Cabelos" com MAIOR discount_percentage.
# Imprima apenas as colunas "name" e "discount_percentage".

# TODO: seu código aqui

df_produtos = df[df['normalized_category'] == "Cabelos"]
df_sorted = df_produtos.sort_values(
    by='promotional_price',
    ascending=True
)
print(df_sorted.head(3))


# ═══════════════════════════════════════════════════════════════════════════
# TAREFA 6 — Agrupamento (1,5 pts)
# ═══════════════════════════════════════════════════════════════════════════
# Use groupby em "normalized_category" para calcular:
#   - preço promocional médio  (coluna: preco_medio)
#   - quantidade de produtos   (coluna: qtd_produtos)
#
# Ordene pelo preco_medio (do maior para o menor) e mostre o resultado completo.
# Qual categoria tem o preço promocional médio mais alto? Imprima o nome dela.

# TODO: seu código aqui

df_agrupado = df.groupby('normalized_category').agg(
    preco_medio = ('promotional_price', 'mean'),
    qtd_produtos = ('promotional_price', 'count')
)
print(df_agrupado)

# ═══════════════════════════════════════════════════════════════════════════
# TAREFA 7 — Limpeza de dados (1 pt)
# ═══════════════════════════════════════════════════════════════════════════
# O dataset tem produtos repetidos (mesmo `code` em linhas diferentes).
# a) Imprima quantas linhas existem ANTES de remover duplicatas.
# b) Remova duplicatas mantendo apenas a primeira ocorrência de cada `code`.
# c) Imprima quantas linhas restaram DEPOIS.

# TODO: seu código aqui

df_linhas = df.shape
print(f"\nEssa é a quantidade de linhas presente nessa base: {df_linhas[0]}")
df_sem_duplicatas = df.drop_duplicates(
    subset='code',
    keep='first'
)
print(df_sem_duplicatas)
print(df_sem_duplicatas.shape)


# ═══════════════════════════════════════════════════════════════════════════
# TAREFA 8 — Filtro combinado (1,5 pts)
# ═══════════════════════════════════════════════════════════════════════════
# Filtre produtos que:
#   - têm "Vegano" na coluna features (dica: use .str.contains("Vegano", na=False))
#   - estão em promoção (promotion_active == True)
#   - têm desconto maior que 40% (discount_percentage > 40)
#
# Imprima:
#   a) Quantos produtos atendem aos 3 critérios
#   b) O nome e o desconto do produto com maior discount_percentage nesse grupo

# TODO: seu código aqui
filtro_vegano = df['features'].str.contains("Vegano", na=False)

filtro_promocao = df['promotion_active'] == True

filtro_desconto = df['discount_percentage'] > 40

df_vegano = df[
    filtro_vegano &
    filtro_promocao & 
    filtro_desconto
    ]

print(f"Essa foi a quantidade de produtos encontrados: {df_vegano.shape[0]}")

df_ordenado = df_vegano.sort_values(
    by='discount_percentage',
    ascending=False
)

print(df_ordenado[['catalog_name', 'discount_percentage']].head(1))

# ═══════════════════════════════════════════════════════════════════════════
# DESAFIO FINAL — BÔNUS (2 pts)
# ═══════════════════════════════════════════════════════════════════════════
# Monte um "relatório da linha Malbec" com as seguintes informações:
#
#   1. Total de produtos da linha "Malbec"
#   2. Quantos estão em promoção
#   3. Preço promocional médio da linha
#   4. Produto com maior desconto (nome + percentual)
#   5. Categoria (normalized_category) mais frequente entre os produtos Malbec
#
# Dica: você pode usar filtros, groupby, value_counts e sort_values juntos.
# Formate a saída de forma legível, como um mini-relatório em texto.

# TODO: seu código aqui

# RELATÓRIO DA LINHA MALBEC

# 1. Filtrar produtos da linha Malbec
Filtro_Malbec = df['product_line'] == "Malbec"

df_malbec = df[Filtro_Malbec]


# 2. Filtrar produtos Malbec em promoção
Filtro_promocao = df_malbec['promotion_active'] == True

df_malbec_promocao = df_malbec[Filtro_promocao]


# 3. Calcular o preço promocional médio
df_promocao = df_malbec_promocao['promotional_price'].mean()


# 4. Encontrar o produto com maior desconto
df_maior_desconto = df_malbec.sort_values(
    by='discount_percentage',
    ascending=False
)

maior_desconto = df_maior_desconto.iloc[0]


# 5. Identificar a categoria mais frequente
categoria = df_malbec['normalized_category'].value_counts()

categoria_mais_frequente = categoria.index[0]

quantidade_categoria = categoria.iloc[0]


# 6. Gerar o relatório
print("=" * 50)
print("          RELATÓRIO DA LINHA MALBEC")
print("=" * 50)

print(f"Total de produtos Malbec: {len(df_malbec)}")

print(f"Produtos em promoção: {len(df_malbec_promocao)}")

print(f"Preço promocional médio: R$ {df_promocao:.2f}")

print(
    f"Produto com maior desconto: {maior_desconto['name']} "
    f"({maior_desconto['discount_percentage']:.2f}%)"
)

print(
    f"Categoria mais frequente: {categoria_mais_frequente} "
    f"({quantidade_categoria} produtos)"
)

print("=" * 50)
