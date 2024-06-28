from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
import time
import os
from selenium.webdriver.common.by import By
from ePCA import ultis

from ePCA.Model import cidadeAnoSatus as SQLcidadeAnoStatus


def acessarSegundaTela(driver,diretorio):
    '''
    a = driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/table/tbody[1]/tr[2]/td/div/div/div[3]/table/tbody[1]/tr/td[4]/div/button')
    a.click()
    time.sleep(3)
    b = driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div/div[3]/table/tbody[1]/tr[1]/td[3]/div/button')
    b.click()
    time.sleep(3)
    resultadoBaixarArquivo =  ultis.download(diretorio)
    if resultadoBaixarArquivo:
        print("Último arquivo baixado:", resultadoBaixarArquivo)
    else:
        print("Nenhum arquivo foi baixado dentro do tempo limite.")
    '''
    indentificarSegundaTabela(driver)
    return

def indentificarLinhasDaPrimeiraTabela():
    return

def indentificarSegundaTabela(driver):
    #a = driver.find_element(By.XPATH,'/html/body/div/div[4]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div')

    soup = transformarDriveEmTextoHtml(driver)
    # Pegando o numero de itens na tabela
    listNames = soup.select('.z-listbox-body')

    #listNames = listNames[2].find_all('tr','z-listitem')
    '''
    listaDeTipo = []
    listaDeSubtipos = []
    listaCompleta = {}
    for tr in listNames:
        lista_th = tr.find('th')
        if lista_th:
            nameTipoChave = lista_th.text
            listaDeTipo.append(nameTipoChave)
            listaCompleta[nameTipoChave] = []
        else:
            nameSubTipo = tr.text
            listaDeSubtipos.append(nameSubTipo)
            ultimoTipoAdicionado = listaDeTipo[-1]
            listaCompleta[ultimoTipoAdicionado].append(nameSubTipo)

    print(listaCompleta)
    '''
    contagoverno = soup.select('.z-groupbox-content')
    #print(contagoverno)
    contagovernoHeader = contagoverno[0].find_all('div','z-listbox-header')
    contagovernoBody = contagoverno[0].find_all('div','z-listbox-body')
    header = contagovernoHeader[0].find_all('div','z-listheader-content')
    body = contagovernoBody[0].find_all('div','z-listcell-content')
    print(header[0].text)
    print(body[0].text)










    driver.quit()
    time.sleep(500)
    return
def transformarDriveEmTextoHtml(driver):
    # Obter o código HTML da página
    html = driver.page_source
    # Analisar o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return soup


'''
# Imprimir os resultados
for th_text in listaDeTipo:
    print(th_text)
print(listaDeTipo.__len__())

for th_text in listaDeSubtipos:
    print(th_text)
print(listaDeSubtipos.__len__())
'''
#/html/body/div/div[4]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/table/tbody[1]/tr[1]/td/div/div/div[3]/table/tbody[1]/tr[1]/td[4]/div/button
#/html/body/div/div[4]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/table/tbody[1]/tr[2]/td/div/div/div[3]/table/tbody[1]/tr[1]/td[4]/div/button