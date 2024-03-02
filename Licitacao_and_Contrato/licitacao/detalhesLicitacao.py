from Licitacao_and_Contrato.licitacao import tabelasDetalhesLicitação
from Ultils.pastas.pastasModulos import licitacao as criarPasta
from Ultils import gerarArquivo
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os



def mostrarDetalhe(driver,directoryInformation,link):
    dadosTabela = {}
    print("Acessando: ", link)
    directory = directoryInformation["licitacaoFolder"]
    # Criar uma pasta geral
    if not os.path.exists(directory):
        os.makedirs(directory)


    # Navegar até a página
    driver.get(link)
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
            if input.find("label"):
                if input.find("label").text == "Objeto: ":
                    dadosTabela["Objeto"] = []
                    valorObjeto = input.find("textarea").text
                    dadosTabela["Objeto"].append(valorObjeto)

                    ##Dados que não seguem o mesmo padrão no HTML
                    # Natureza de despesa:
                    # Objeto:
                elif input.find("label").text == "Natureza de despesa: ":
                    dadosTabela["Natureza de despesa"] = []
                    valorObjeto = input.find("textarea").text
                    dadosTabela["Natureza de despesa"].append(valorObjeto)
                else:
                    print('')

    # Validar
    if 'Nº Processo ' in dadosTabela and dadosTabela['Nº Processo '][0] is not None and dadosTabela['Nº Processo '][
        0] != "":
        numeroProcesso = dadosTabela['Nº Processo '][0]
    else:
        numeroProcesso = ''

    dadosName = {"numero": numeroProcesso, "link": link}

    # Criar uma pasta e arquivo json com dados
    namefolder = criarPasta(dadosName, directory)



    gerarArquivo.criarCSV(dadosTabela, namefolder + '/Detalhes da licitação')
    gerarArquivo.editarCSV(dadosTabela, directoryInformation["licitacaoFolder"]+'/Todas as licitações')
    #time.sleep(2)

    tabelasDetalhesLicitação.verificarSeExisteTabelas(soup, namefolder)



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





