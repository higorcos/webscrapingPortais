from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
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
    #voltarParaPaginaPrincipal(driver)

    resultadoTabela = indentificarSegundaTabela(driver)
    for tipoId, (tipoPrincipal, todosOsSubTipos) in enumerate(resultadoTabela.items(), 1):
        for subTipoId, subTipo in enumerate(todosOsSubTipos, 1):
            '''
            print(f"Posição pai: {tipoId}")
            print(f"Nome Pai: {tipoPrincipal}")
            print(f"Posição Filho: {subTipoId}")
            print(f"Nome Filho: {subTipo.strip()}")
            print("-" * 100)
            '''
            numeroTabela = str(tipoId)
            numeroLinhaDaTabela = str(subTipoId)
            #numeroTabela = str(4)
            #numeroLinhaDaTabela = str(1)
            stringPath = f'/html/body/div/div[4]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/table/tbody[1]/tr[{numeroTabela}]/td/div/div/div[3]/table/tbody[1]/tr[{numeroLinhaDaTabela}]/td[4]/div/button'

            abrirBoxDeArquivosParaBaixar(driver,stringPath)

            fecharBoxDeArquivosParaBaixar(driver)

    driver.quit()

    return
def indentificarSegundaTabela(driver):
    soup = transformarDriveEmTextoHtml(driver)
    # Pegando o numero de itens na tabela
    listNames = soup.select('.z-listbox-body')
    listNames = listNames[2].find_all('tr', 'z-listitem')
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

    return listaCompleta



    #abrirBoxDeArquivosParaBaixar(driver)
    #verificar se box existe
    #verificarBox = verificarSeExisteBoxDosArquivosParaBaixar(driver)
    #if verificarBox:
        #print('Existe')




    driver.quit()
    time.sleep(500)
    return
def indentificarLinhasDaPrimeiraTabela(soup):
    contagoverno = soup.select('.z-groupbox-content')
    #print(contagoverno)
    contagovernoHeader = contagoverno[0].find_all('div','z-listbox-header')
    contagovernoBody = contagoverno[0].find_all('div','z-listbox-body')
    header = contagovernoHeader[0].find_all('div','z-listheader-content')
    body = contagovernoBody[0].find_all('div','z-listcell-content')
    print(header[0].text)
    print(body[0].text)
    return
def verificarSeExisteBoxDosArquivosParaBaixar(driver):
    resutado = verificarSeExisteBoxDeErro(driver)
    if not resutado:
        try:
            element = driver.find_element(By.XPATH, "/html/body/div[2]")
            # Obter o HTML do elemento
            element_html = element.get_attribute('outerHTML')

            # Usar BeautifulSoup para analisar o HTML do elemento
            soup = BeautifulSoup(element_html, 'html.parser')
            element_soup = soup.find()

            # Verificar se o estilo contém display: none
            is_display_none = 'display: block' in element_soup.get('style', '')

            if is_display_none:
                #print("O elemento está visivel")
                element_exists = True
            else:
                #print("O elemento não está visivel")
                element_exists = False
            return element_exists
        except NoSuchElementException:
            #print("Elemento não existe !!")
            element_exists = False
            return element_exists
    else:
        return False
def abrirBoxDeArquivosParaBaixar(driver,stringPath):
    try:
        box = driver.find_element(By.XPATH,stringPath)
        box.click()
        time.sleep(5)
        return True
    except NoSuchElementException:
        print("Elemento não encontrado: Função abrirBoxDeArquivosParaBaixar() ")
        return False
def fecharBoxDeArquivosParaBaixar(driver):
    resultado = verificarSeExisteBoxDosArquivosParaBaixar(driver)
    if resultado:
        try:
           box = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div')
           box.click()
           time.sleep(2)
           return True
        except NoSuchElementException:
            print("Elemento não encontrado: Função fecharBoxDeArquivosParaBaixar() ")
            return False
    else:
        return False

def verificarSeExisteBoxDeErro(driver):

    try:
        button = driver.find_element(By.XPATH, "//button[text()='OK']")
        button.click()
        return True
    except NoSuchElementException:
        return False
def transformarDriveEmTextoHtml(driver):
    # Obter o código HTML da página
    html = driver.page_source
    # Analisar o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return soup
def voltarParaPaginaPrincipal(driver):
    time.sleep(5)
    try:
        sair = driver.find_element(By.XPATH, "//button[text()='Voltar']")
        sair.click()
        time.sleep(0.6)
        return True
    except NoSuchElementException:
        print("O botão 'OK' não existe.")
        return False

'''
# Imprimir os resultados
for th_text in listaDeTipo:
    print(th_text)
print(listaDeTipo.__len__())

for th_text in listaDeSubtipos:
    print(th_text)
print(listaDeSubtipos.__len__())
'''


'''
/html/body/div[6]/div/div - Card processamento 

/html/body/div[7]/div[1]/div   - Botão de close do erro depois do processamento 

/html/body/div[7] - Erro depois do processamento do click 





'''