from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
from Ultils import gerarArquivo, downloadArquivos


def andamento(driver):
    linkPortal = "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/detalhes/991136499";
    nomePortal = "Mirador";
    tipoPortal = "PM";
    tipoArquivosDownloads = "Andamentos da Licitação";

    print("Download arquivos de andamento da Licitação")

    # Criar uma pasta para os downloads (se ela ainda não existir)
    download_dir = 'Downloads-' + tipoArquivosDownloads;

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    driver.get(linkPortal)

    # Aguardar o carregamento da página
    time.sleep(1)

    # Obter o código HTML da página
    html = driver.page_source

    # Analisar o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Tag da tabela
    table = soup.select('.col-xs-12')
    #table = soup.select('.col-xs-12+ .col-xs-12')
    # print(table)
    lines = table[0].find_all("tr")
    linesTitle = lines[0].find_all("th")
    # Remover titulos das colunas
    lines.pop(0)
    # print(lines)

    title0 = linesTitle[0].text
    title1 = linesTitle[1].text
    title2 = linesTitle[2].text
    title3 = linesTitle[3].text

    dadosTabela = {title0:[], title1:[], title2:[],title3:[],"status":[]}


    for i in range(0, lines.__len__()):
        colums = lines[i].find_all()
        colum0 = colums[0].text
        colum1 = colums[1].text
        colum2 = colums[2].text #data
        colum3 = colums[3].find('a').get('href') #link
        link = colum3

        #print(colum0, colum1, colum2, colum3)
        print("\tTIPO: " +  colum0 );


        # Criar uma pasta individual para o arquivo baixado dentro da pasta de downloads
        number0 = str(i)
        dateFileNewFormat = colum2.replace('/', '-').replace(':', '.')  # remover barra e dois pontos
        newDir = "TIPO " +  colum0 + " DESCRICAO " +  colum1 + " DATA "+dateFileNewFormat + "" +number0
        file_dir = os.path.join(download_dir, newDir)

        # Verificar se encontrou a tag <a>
        if link:
            statusDonwload = downloadArquivos.link(link, file_dir)
        else:
            print("\tLink não encontrado")
            statusDonwload = {'status Donwload': "Link não foi passado"}

        #print("\tTIPO: " +  colum0 + " DESCRICAO: " +  colum1 + " DATA ENVIO: " +colum2 + " LINK: "+ colum3 + ' Status: ', statusDonwload['status Donwload']);
        #print("\tTIPO: " +  colum0 + ' Status: ', statusDonwload['status Donwload']);


        dadosTabela[title0].append(colum0)
        dadosTabela[title1].append(colum1)
        dadosTabela[title2].append(colum2)
        dadosTabela[title3].append(colum3)
        dadosTabela["status"].append(statusDonwload['status Donwload'])


    gerarArquivo.CSV(dadosTabela, "Resumo"+download_dir);
    # Fechar o navegador
    driver.quit()
    return []


def contratos():
    # Criar uma nova instância do driver do Chrome
    driver = webdriver.Chrome()

    # Definir o tamanho da janela
    driver.set_window_size(800, 600);
    # Navegar até a página
    andamento(driver)

contratos()
