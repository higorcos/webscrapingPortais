from Licitacao_and_Contrato.licitacao import tabelasDetalhesLicitação
from Ultils import gerarArquivo
from selenium import webdriver
from bs4 import BeautifulSoup
import random
import time
import os
import re


# Registra o tempo de início
inicio = time.perf_counter()

def mostrarDetalhe(driver,directoryInformation,link):
    dadosTabela = {}

    # Criar uma pasta geral
    if not os.path.exists(directoryInformation["licitacaoFolder"]):
        os.makedirs(directoryInformation["licitacaoFolder"])


    # Navegar até a página
    driver.get(link)

    # Aguardar o carregamento da página
    time.sleep(1)

    # Obter o código HTML da página
    html = driver.page_source

    # Analisar o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    #Informações das licitações
    selectDivs = soup.select('.form-group')

    for input in selectDivs:

        if (input.find("input")):
            chave = input.find("label").text
            valor = input.find("input")["value"]
            dadosTabela[chave] = []
            dadosTabela[chave].append(valor)

        else:
            print("")
    ##Dados que não seguem o mesmo padrão no HTML
        #Natureza de despesa:
        #Objeto:
    naturezaDespesa = soup.select('.col-md-2+ .col-md-12')
    objeto = soup.select('.col-md-4+ .col-md-12')

    chaveNaturezaDespesa = naturezaDespesa[0].find("label").text
    valorNaturezaDespesa = naturezaDespesa[0].find("textarea").text

    dadosTabela[chaveNaturezaDespesa] = []
    dadosTabela[chaveNaturezaDespesa].append(valorNaturezaDespesa)

    chaveObjeto = objeto[0].find("label").text
    valorObjeto = objeto[0].find("textarea").text

    dadosTabela[chaveObjeto] = []
    dadosTabela[chaveObjeto].append(valorObjeto)


    # Use uma expressão regular para encontrar o número na URL
    numeroDoLink = re.search(r'(\d+)$', link).group(1)
    # Numero do processo
    numberProcesso = dadosTabela['Nº Processo '][0]
    numberProcesso = numberProcesso.replace('/', '-').replace(':', '.') #remover barra e dois
    namefolder = directoryInformation["licitacaoFolder"] +"/"+ "Nº "+ numberProcesso +"  ID-"+numeroDoLink


    # Criar uma pasta para cada licitação
    if not os.path.exists(namefolder):
        os.makedirs(namefolder)

    gerarArquivo.criarCSV(dadosTabela, namefolder + '/Detalhes da licitação')
    gerarArquivo.editarCSV(dadosTabela, directoryInformation["licitacaoFolder"]+'/Todas as licitações')
    #time.sleep(2)
    print("Acessando: ",link)

    tabelasDetalhesLicitação.verificarSeExisteTabelas(soup, namefolder)

    fim = time.perf_counter()
    tempo_total = fim - inicio

    print("tempo de execução", tempo_total)




def runMostrarDetalhe():

    #link = "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/detalhes/991136499";
    link="https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/detalhes/991136323"
    nomePortal = "Mirador";
    tipoPortal = "PM";

    directoryInformation = {
        "mainFolder": "Downloads-" + nomePortal + "-" + tipoPortal + "",
        "licitacaoFolder": "Licitações e Contratos",
    }

    # Criar uma nova instância do driver do Chrome

    driver = webdriver.Chrome()
    driver.set_window_size(800, 600);

    driver.get(link)

    driver2 = webdriver.Chrome()
    time.sleep(2)
    driver2.get(link)

    #mostrarDetalhe(driver, directoryInformation, link)
    # Fechar o navegador
    driver.quit()

#runMostrarDetalhe();





