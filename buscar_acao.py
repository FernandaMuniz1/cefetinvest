

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://www.fundamentus.com.br/resultado.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}

def scrape_data(url):
    """
    Realiza a limpeza dos dados do DataFrame data_frame, 
    removendo caracteres indesejados e convertendo
    as colunas específicas para o tipo float.

    Args:
        data_frame (pandas.DataFrame): DataFrame contendo os dados a serem limpos.

    Returns:
        pandas.DataFrame: DataFrame com os dados limpos.
    """
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tabela_html = soup.find('table')
        return pd.read_html(str(tabela_html))[0]
    else:
        print("Erro ao acessar a página")
        return None

def clean_data(data_frame):
    """
    Salva o DataFrame data_frame em um arquivo Excel com o nome especificado.

    Args:
        data_frame (pandas.DataFrame): DataFrame a ser salvo.
        filename (str): Nome do arquivo Excel a ser criado.

    Returns:
        None
    """
    columns_to_clean = ['Cotação','P/L', 'P/VP', 'PSR', 'Div.Yield','P/Ativo',	'P/Cap.Giro',	'P/EBIT',	'P/Ativ Circ.Liq',	'EV/EBIT',
                        	'EV/EBITDA', 'Liq. Corr.']
    data_frame[columns_to_clean] = data_frame[columns_to_clean].astype(str).apply(lambda x: x.str.replace(
        '%', '').str.replace(',', '').str.replace('.', ''))
    data_frame[columns_to_clean] = data_frame[columns_to_clean].astype(float)
    data_frame.rename(columns={'Div.Yield': 'DY', 'Cotação': 'PRECO', 'EV/EBIT': 'DIVIDA LIQUIDA / EBIT'}, inplace=True)
    data_frame['PRECO'] = data_frame['PRECO'] / 100
    data_frame['DY'] = data_frame['DY'] / 100
    data_frame['P/VP'] = data_frame['P/VP'] / 100
    data_frame['P/VP'] = data_frame['P/VP'].round(2)
    data_frame['P/L'] = data_frame['P/L'] / 100
    data_frame['PSR'] = data_frame['PSR'] / 100
    data_frame['P/Ativo'] = data_frame['P/Ativo'] / 100
    data_frame['P/Cap.Giro'] = data_frame['P/Cap.Giro'] / 100
    data_frame['P/EBIT'] = data_frame['P/EBIT'] / 100
    data_frame['P/Ativ Circ.Liq'] = data_frame['P/Ativ Circ.Liq'] / 100
    data_frame['DIVIDA LIQUIDA / EBIT'] = data_frame['DIVIDA LIQUIDA / EBIT'] / 100
    data_frame['EV/EBITDA'] = data_frame['EV/EBITDA'] / 100
    return data_frame

data_frame_fii = scrape_data(URL)
if data_frame_fii is not None:
    data_frame_final = clean_data(data_frame_fii)
    data_frame_final = data_frame_final[data_frame_final['Liq. Corr.'] != 0]
    # Apagar as linhas onde a coluna "Liquidez" é igual a 0.0
    # O parâmetro index=False evita a gravação do índice no arquivo
    data_frame_final.to_excel('acoes.xlsx', index=False)