from Licitacao_Siganet.contrato import tabelasDetalhesContrato
from Ultils.pastas.pastasModulos import contrato as  criarPasta
from selenium.webdriver.chrome.options import Options
from Ultils import gerarArquivo
from selenium import webdriver
from bs4 import BeautifulSoup
import concurrent.futures
import time
import os
import re

directoryGlobal = ''

def acessarPaginaDetalhes(table,directory,titles,dadosTabela):
    global directoryGlobal
    directoryGlobal = directory

    title0 = titles[0]
    title1 = titles[1]
    title2 = titles[2]
    title3 = titles[3]
    title4 = titles[4]
    title5 = titles[5]

    with concurrent.futures.ThreadPoolExecutor() as executor:
            result = executor.map(mostrarDetalhe,table)

    for dados in result:
        dadosTabela[title0].append(dados[0])
        dadosTabela[title1].append(dados[1])
        dadosTabela[title2].append(dados[2])
        dadosTabela[title3].append(dados[3])
        dadosTabela[title4].append(dados[4])
        dadosTabela[title5].append(dados[5])

    print("\t-------Finalizou Contratos")
    return dadosTabela

def mostrarDetalhe(line):
    dadosTabela={}

    colums = line.find_all()
    colum0 = colums[0].text #Nº Instrumento
    colum1 = colums[1].text #Nº Contrato
    colum2 = colums[2].text #Objeto
    colum3 = colums[3].text #CNPJ
    colum4 = colums[4].text #Razão Social
    colum5 = colums[5].find('a').get('href')  #Detalhes(link)
    link = colum5

    #abrir link
    # Configurações para executar o Chrome em modo headless
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Ativa o modo headless
    driver = webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Chrome()
    driver.set_window_size(800, 600);
    driver.get(link)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    #Pegar campos
    selectDivs = soup.select('.form-group')


    for input in selectDivs:

        if (input.find("input")):
            chave = input.find("label").text
            valor = input.find("input")["value"]
            dadosTabela[chave] = []
            dadosTabela[chave].append(valor)
        else:
            if input.find("label"):
                if input.find("label").text == "Objeto: ":
                    dadosTabela["Objeto"] = []
                    valorObjeto = input.find("textarea").text
                    dadosTabela["Objeto"].append(valorObjeto)

    dadosTabela["link"] = []
    dadosTabela["link"].append(link)

    #Validar
    if 'Nº Contrato' in dadosTabela and dadosTabela['Nº Contrato'][0] is not None and dadosTabela['Nº Contrato'][
        0] != "":
        numeroContrato = dadosTabela['Nº Contrato'][0]
    else:
        numeroContrato = ''

    dadosName = {"numero":numeroContrato,"link":link }

    # Criar uma pasta e arquivo json com dados
    namefolder = criarPasta(dadosName, directoryGlobal)


    gerarArquivo.criarCSV(dadosTabela, namefolder + '/Detalhes do contrato')

    tabelasDetalhesContrato.verificarSeExisteTabelas(soup, namefolder)
    driver.quit()

    return [colum0,colum1,colum2,colum3,colum4,link]





#VERIFICAR ERRO OBJETO





