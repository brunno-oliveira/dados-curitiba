import pandas as pd
from bs4 import BeautifulSoup
from urllib3 import poolmanager
import re

def getDownloadUrls(cnnBuilder):
    """ Acessa a repositório que contém os links para as bases de despesas e receitas
        e passa todos os links para dois arrays: arrDespesa e arrRceita"""
        
    url = 'http://dadosabertos.c3sl.ufpr.br/curitiba/BaseReceitaDespesa/'
        
    html = cnnBuilder.urlopen('GET', url)    
    soup = BeautifulSoup(html.data)
    
    arrDespesa = []
    arrReceita = []
    
    for a in soup.find_all('a'):    
        if(a.get_text().find('Receitas') > -1):
            arrReceita.append(url + a.get_text())
        elif(a.get_text().find('Despesas') > -1): 
            arrDespesa.append(url + a.get_text())

    return arrDespesa
        
def downloadCsv(cnnBuilder, arrDespesa):
    """ Baixa todos os arquivos do array e salva separadamente """
    for url in arrDespesa:
        if('csv' in url): # O dicionário em XLSX
            file_name = str(re.findall('/20.*-.*-.*_', arrDespesa[1]))[2:14] + '.csv'
            r = cnnBuilder.request('GET', url, preload_content=False)
            with open(file_name, 'wb') as out:
                while True:
                    data = r.read(64)
                    if not data:
                        break
                    out.write(data)

def __init__():
    connectBuilder = poolmanager.PoolManager()    
    arrDespesa = getDownloadUrls(connectBuilder)
    downloadCsv(connectBuilder, arrDespesa)        
    connectBuilder.clear()
