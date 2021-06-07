import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://pt.wikipedia.org/wiki/Lista_de_c%C3%B3digos_de_pa%C3%ADs_GS1"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

# pega a tabela com códigos
tabela_codigos = soup.find(name='table')
itens_tabela = tabela_codigos.find_all('tr')

paises = []
codigos_gs1 = []
dic_codigos_pais = {}

def normaliza_codigo(codigo):
    lista_codigos = []

    codigo_normal = ''
    for letra in codigo:
        if letra.isdigit():
            codigo_normal += letra

    if len(codigo) > 3:
        lista_codigos.append(codigo_normal[0:3])
        lista_codigos.append(codigo_normal[3:8])
    else:
        lista_codigos.append(codigo_normal)

    return lista_codigos

def normaliza_pais(pais):
    try:
        if 'GS1' in pais:
            pais = pais.split('GS1 ')[1].split('\n')[0]
        if ' -' in pais:
            pais = pais.split(' -')[0]
        if '</' in pais:
            pais = ''

    except IndexError:
        pais = ''

    return pais

for i in range(1,len(itens_tabela)):
    item = itens_tabela[i]
    codigos = item.prettify().split('<td>')[1][3:12].split('\n </td')[0].strip()
    lista_codigos = normaliza_codigo(codigos)

    pais = normaliza_pais(item.prettify().split('td>')[5])
    
    if pais != '':
        for codigo in lista_codigos:
            codigos_gs1.append(codigo)
            paises.append(pais)
    

dic_codigos_pais['codigo_gs1'] = codigos_gs1
dic_codigos_pais['pais'] = paises

codigos_gs1 = pd.DataFrame(dic_codigos_pais)
codigos_gs1.to_csv('./dados/codigos_gs1.csv')