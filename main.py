"""
    Imports
"""

import requests
from bs4 import BeautifulSoup
import locale
from tabulate import tabulate
from models import FundoImobiliario, Estrategia

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def trata_porcentagem(porcentagem_str):
    return locale.atof(porcentagem_str.split('%')[0])


def trata_decimal(decimal_str):
    return locale.atof(decimal_str)

headers={'User-Agent': 'Mozilla/5.0'}

# Armazena dados do site
resposta = requests.get('https://www.fundamentus.com.br/fii_resultado.php', headers=headers)

soup = BeautifulSoup(resposta.text, 'html.parser')

# Filtra somente as linhas da tabela
linhas = soup.find(id="tabelaResultado").find('tbody').find_all('tr')

resultado = []

estrategia = Estrategia(
    cotacao_atual_minima=50.0,
    dividiend_yield_minimo=5,
    p_vp_minimo=0.70,
    valor_mercado_minimo=100000000,
    liquidez_minima=50000,
    qt_minima_imoveis=5,
    maxima_vacancia_media=10
)

for linha in linhas:
    # Armazena os dados da linha
    dados_fundo = linha.find_all('td')
    
    # Armazena dado a dado
    codigo = dados_fundo[0].text
    segmento = dados_fundo[1].text
    cotacao = trata_decimal(dados_fundo[2].text)
    ffo_yield = trata_porcentagem(dados_fundo[3].text)
    dividiend_yield = trata_porcentagem(dados_fundo[4].text)
    p_vp = trata_decimal(dados_fundo[5].text)
    valor_mercado = trata_decimal(dados_fundo[6].text)
    liquidez = trata_decimal(dados_fundo[7].text)
    qt_imoveis = int(dados_fundo[8].text)
    preco_m2 = trata_decimal(dados_fundo[9].text)
    aluguel_m2 = trata_decimal(dados_fundo[10].text)
    cap_rate = trata_porcentagem(dados_fundo[11].text)
    vacancia = trata_porcentagem(dados_fundo[12].text)
    
    fundo_imobiliario = FundoImobiliario(
        codigo, segmento, cotacao, ffo_yield, dividiend_yield, p_vp, 
        valor_mercado, liquidez, qt_imoveis, preco_m2, aluguel_m2, cap_rate, vacancia
    )

    if estrategia.aplica_estrategia(fundo_imobiliario):
        resultado.append(fundo_imobiliario)
        
cabecalho =["Código", "Segmento", "Cotação Atual", "Dividend Yield"]

tabela = []

for elemento in resultado:
    tabela.append([
        elemento.codigo, 
        elemento.segmento, 
        locale.currency(elemento.cotacao_atual), 
        f'{locale.str(elemento.dividiend_yield)} %'
    ])

print(tabulate(tabela, headers=cabecalho, showindex='always', tablefmt='fancy_grid'))
