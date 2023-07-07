import streamlit as st
import yfinance as yf
from PIL import Image
from datetime import date
import pandas as pd

df = pd.read_excel('acoes.xlsx')

#Seleciona as colunas que sofrerão modificações
# e após o parse para float será deslocada a vírgula novamente para esquerda 
# para trazer para o padrão brasileiro
columns_to_clean = ['P/VP', 'PRECO', 'DIVIDA LIQUIDA / EBIT', 'P/L']
df[columns_to_clean] = df[columns_to_clean].applymap(lambda x: float(str(x).replace('.', '').replace(',', '.'))/1000)


#pega os valores da planilha pelas colunas
maior_preco = df['PRECO'].max()
menor_preco = df['PRECO'].min()

# configs da pagina
st.set_page_config(
    page_title="CEFETINVEST",
    page_icon="",
    #layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.google.com'
    }
)

#barra lateral
with st.sidebar:
    st.header('Filtro de Ações')
   
    # Insere o campo de entrada para o preço máximo
    preco_maximo = st.number_input('Preço máximo:', min_value=menor_preco, max_value=maior_preco)
    st.write('Minimo:', menor_preco, ' Máximo:', maior_preco)
    st.write('---')

    dy_filtro = st.slider('DY entre:', float(df['DY'].min()), float(df['DY'].max()), (float(df['DY'].min()), float(df['DY'].max())))
    filtro_pvp = st.slider('P/VP entre:', float(df['P/VP'].min()), float(df['P/VP'].max()), (float(df['P/VP'].min()), float(df['P/VP'].max())))
    pvp_menor, pvp_maior = filtro_pvp

    filtro_pl = st.slider('Preço/Lucro entre:', float(df['P/L'].min()), float(df['P/L'].max()), (float(df['P/L'].min()), float(df['P/L'].max())))
    pl_menor, pl_maior = filtro_pl

    filtroDL = st.slider('Dívida Líquida/EBITDA entre:', float(df['DIVIDA LIQUIDA / EBIT'].min()), float(df['DIVIDA LIQUIDA / EBIT'].max()),
                          (float(df['DIVIDA LIQUIDA / EBIT'].min()), float(df['DIVIDA LIQUIDA / EBIT'].max())))
    DL_menor, DL_maior = filtroDL
# colocando o logo da obinvest
logo=Image.open('./imagens/OBInvestLogo.png')
st.image(logo)
st.divider()

# Variável de controle para exibir o DataFrame filtrado ou completo
EXIBIR_DF_FILTRADO = False

# Botões "Filtrar" e "Limpar"
if st.sidebar.button(":green[Filtrar]"):
    EXIBIR_DF_FILTRADO = True

if st.sidebar.button(":red[Limpar]"):
    EXIBIR_DF_FILTRADO = False
    # Limpa as seleções de filtro   
    dy_filtro = 0.0
    preco_maximo = 0.0
    pvp_menor = 0.0
    pvp_maior = 0.0
    pl_menor  = 0.0
    pl_maior = 0.0
    DL_menor = 0.0
    DL_maior  = 0.0
# Verifica se o botão "Filtrar" foi clicado
if EXIBIR_DF_FILTRADO:
    # Filtra a coluna DY com base no valor selecionado  E Filtra a coluna "preço" com base no preço máximo
    acoes_filtradas = df[
    (df['DY'].between(dy_filtro[0], dy_filtro[1])) &
    (df['PRECO'] <= preco_maximo) &
    (df['P/VP'].between(pvp_menor, pvp_maior)) &
    (df['P/L'].between(pl_menor, pl_maior)) &
    (df['DIVIDA LIQUIDA / EBIT'].between(DL_menor, DL_maior))]
        


    # Seleciona as colunas desejadas
    colunas_selecionadas = ['Papel','PRECO' , 'DY', 'P/VP', 'P/L', 'DIVIDA LIQUIDA / EBIT']
    df_filtrado = acoes_filtradas[colunas_selecionadas]
    st.dataframe(df_filtrado,  width=1000, height=600)


else:
 # Exibe o DataFrame completo inicialmente
    colunas_selecionadas_original = ['Papel', 'PRECO', 'DY', 'P/VP', 'P/L', 'DIVIDA LIQUIDA / EBIT']
    df_original = df[colunas_selecionadas_original]
    st.dataframe(df_original, width=1000, height=600)