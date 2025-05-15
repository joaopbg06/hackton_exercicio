import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurações  iniciais
st.set_page_config(page_title="Dashboard financeiro", page_icon="🛒", layout="wide")

# Carregar dados

df_despesas = pd.read_excel('./limpo/despesas_limpo.xlsx')
df_orcamentos = pd.read_excel('./limpo/orcamentos_limpo.xlsx')

# FILTROS
# Sidebar
st.sidebar.header("Selecione os Filtros")

# Filtro por loja
setor = st.sidebar.multiselect(
    "Setores",
    # Opções do filto
    options=df_despesas["setor"].unique(),
    # Opção que vem como por padrão
    default=df_despesas["setor"].unique(),
    # Chave única
    key='setor'
)

# Filtro por produto
trimestre = st.sidebar.slider(
    "Trimestres",
    min_value=min(df_orcamentos['trimestre']),
    max_value=max(df_orcamentos['trimestre']),
    value=(min(df_orcamentos['trimestre']),max(df_orcamentos['trimestre'])),
    key='tri'
)

# Filtrar o Dataframe com as opções selecionadas
df_selecao_despesas = df_despesas.query("setor in @setor and @trimestre[0] <= trimestre <= @trimestre[1]")
df_selecao_orcamentos = df_orcamentos.query("setor in @setor and @trimestre[0] <= trimestre <= @trimestre[1]")


def Graficos():
    # Criar um grafico de barras
    # Mostrando a quant de produtos por lojas
    gasto_por_trimestre = df_selecao_orcamentos.groupby('trimestre', as_index=False)['valor_realizado'].sum()
    fig_linha = px.line(
        gasto_por_trimestre,
        x="trimestre",
        y="valor_realizado",
        title='Gastos por Trimestre',
        labels={"valor_realizado": "Total Gasto"},
        markers=True,
    )


    setor_por_tipo = df_selecao_despesas.groupby(['setor', 'tipo'], as_index=False)['valor'].sum()
    fig_barra= px.bar(
        setor_por_tipo,
        x='setor',
        y= 'valor',
        color= 'tipo',
        title='Custo com base no Setor e Tipo',
        labels={'compra_matéria-prima': "matéria-prima"}

    )

    valor_por_setor = df_despesas.groupby(['mensal', 'setor'], as_index=False)['valor'].sum()
    fig_barra2 = px.bar(
        valor_por_setor,
        x='mensal',
        y='valor',
        color='setor',
        title='Despesas Mensais por setor',
    )


    valor_q1 = df_selecao_despesas['valor'].quantile(0.25)
    valor_q3 = df_selecao_despesas['valor'].quantile(0.75)
    valor_iqr = valor_q3 - valor_q1

    valor_limite_minimo = valor_q1 - 1.5 * valor_iqr
    valor_limite_maximo = valor_q3 + 1.5 * valor_iqr

    outliers_valor_abaixo = df_selecao_despesas[df_selecao_despesas['valor'] < valor_limite_minimo]
    outliers_valor_acima = df_selecao_despesas[df_selecao_despesas['valor'] > valor_limite_maximo]

    graf1, graf2 = st.columns(2)
    with graf1:
        st.plotly_chart(fig_barra2,  use_container_width=True)
    with graf2:
        st.plotly_chart(fig_barra,  use_container_width=True)
    st.markdown('- - -')

    st.plotly_chart(fig_linha,  use_container_width=True)
    st.markdown('- - -')

    st.text('Fornecedor com custo abaixo do esperado:')
    st.write(outliers_valor_abaixo[['fornecedor', 'valor']])
    st.markdown('- - -')

    st.text('Fornecedor com custo acima do esperado:')
    st.write(outliers_valor_acima[['fornecedor', 'valor']])
    st.markdown('- - -')





Graficos()

# python -m streamlit run plotagem.py

