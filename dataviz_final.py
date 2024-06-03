import streamlit as st
import pandas as pd
import plotly.express as px
import sqlalchemy as sqa

# Conectando ao banco de dados
engine = sqa.create_engine("sqlite:///taxa_natalidade.db", echo=True)
conn = engine.connect()

# Carregando dados do banco de dados
df = pd.read_sql('taxa_natalidade.db', con=conn)

# Imagem do aplicativo
st.sidebar.image('https://static.preparaenem.com/conteudo_legenda/c62624d74b28022b934e0aac8fb0ab06.jpg')

# Convertendo a coluna 'Taxa_Natalidade' para tipo numérico
df['Taxa_Natalidade'] = pd.to_numeric(df['Taxa_Natalidade'], errors='coerce')

# Removendo linhas com valores ausentes
df.dropna(subset=['Taxa_Natalidade'], inplace=True)

# Renomear as colunas para remover espaços  
df.columns = ['Lugar_Estado_Soberano', 'Lugar_Estado', 'Entidade', 'Taxa_Natalidade', 'Data']

# Título da aplicação
st.title("Análise da Taxa de Natalidade")

# Tabela de dados completa
st.header("Tabela de Dados Completa")
st.dataframe(df)

# Histograma da Taxa de Natalidade
st.header("Histograma da Taxa de Natalidade")
fig1 = px.histogram(df, x='Taxa_Natalidade', nbins=10, title='Distribuição da Taxa de Natalidade')
st.plotly_chart(fig1)

# Top 5 países por Taxa de Natalidade
st.header("Top 5 Países por Taxa de Natalidade")
top5 = df.nlargest(5, 'Taxa_Natalidade')
fig2 = px.bar(top5, x='Entidade', y='Taxa_Natalidade', title='Top 5 Países por Taxa de Natalidade')
st.plotly_chart(fig2)

# Mapa de Taxa de Natalidade 
st.header("Mapa de Taxa de Natalidade")
fig3 = px.scatter_geo(df, locations="Entidade", locationmode='country names', size='Taxa_Natalidade', title='Mapa de Taxa de Natalidade')
st.plotly_chart(fig3)

# Comparação entre os 10 primeiros e os 10 últimos países em Taxa de Natalidade
st.header("Comparação entre os 10 primeiros e os 10 últimos países em Taxa de Natalidade")
top10 = df.nlargest(10, 'Taxa_Natalidade')
bottom10 = df.nsmallest(10, 'Taxa_Natalidade')
comparison = pd.concat([top10, bottom10])
fig4 = px.bar(comparison, x='Entidade', y='Taxa_Natalidade', color='Taxa_Natalidade', title='Comparação entre os 10 primeiros e os 10 últimos países')
st.plotly_chart(fig4)

# Fechar a conexão com o banco de dados
conn.close()
