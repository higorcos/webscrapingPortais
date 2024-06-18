from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
import os
from Ultils import gerarArquivo, downloadArquivos
from Ultils.pastas.pastasDocumentosDosModulos import andamento as criarPastaJson
from Ultils.pastas.pastasDocumentosDosModulos import documentosDeLicitacao as criarPastaJsonDOC
from Licitacao_Assesi.contrato import detalhesContrato
import concurrent.futures

directoryGlobal = ''
directoryGlobalContratos = ''
globalParentDirectory = ''
def verificarSeExisteTabelas(soup,directory=''):
    tablesObj = {}
    tables = soup.select('#tableDocumentos')
    headerTable = tables[0].find_all("th")
    bodyTable = tables[0].find_all("tbody")
    bodyTable = tables[0].find_all("tr")

    contratosVersaoJulho2024(soup, directory)
    #documentosDaLicitação(tables,directory)
def documentosDaLicitação(table,directory):
    print("\tDownload arquivos de Documentos da Licitação")

    # Criar uma pasta para os downloads (se ela ainda não existir)
    parentDirectory = directory
    directory = directory+"/DocLici"
    global directoryGlobal
    directoryGlobal = directory

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            print(f"A pasta '{directory}' já existe.")
    except Exception as e:
        print(f"\n\n\tErro ao criar a pasta '{directory}': {e} \n\n")

    lines = table[0].find_all("tr")
    linesTitle = lines[0].find_all("th")
    print('\n\n\n ///////////////////////////')



    # Remover titulos das colunas
    lines.pop(0)
    if not lines:
        return []

    title0 = linesTitle[0].text
    title1 = linesTitle[1].text
    title2 = linesTitle[2].text
    title3 = linesTitle[3].text



    dadosTabela = {title0: [], title1: [], title2: [], title3: [], "status": []}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.map(pecorrerDocLicitacao, lines)

        for dados in result:
            dadosTabela[title0].append(dados[0])
            dadosTabela[title1].append(dados[1])
            dadosTabela[title2].append(dados[2])
            dadosTabela[title3].append(dados[3])
            dadosTabela["status"].append(dados[4])

    print("\t\tBaixou Arquivos de Doc")
    gerarArquivo.criarCSV(dadosTabela, parentDirectory+"/Detalhes Doc");
def andamentos(table,directory):
    print("\tDownload arquivos de andamento da Licitação")

    # Criar uma pasta para os downloads (se ela ainda não existir)
    parentDirectory = directory
    directory = directory+"/Andamento"
    global directoryGlobal
    directoryGlobal = directory

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            print(f"A pasta '{directory}' já existe.")
    except Exception as e:
        print(f"\n\n\tErro ao criar a pasta '{directory}': {e} \n\n")

    lines = table.find_all("tr")
    linesTitle = lines[0].find_all("th")
    # Remover titulos das colunas
    lines.pop(0)
    if not lines:
        return []

    title0 = linesTitle[0].text
    title1 = linesTitle[1].text
    title2 = linesTitle[2].text
    title3 = linesTitle[3].text

    dadosTabela = {title0: [], title1: [], title2: [], title3: [], "status": []}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.map(pecorrerLinhasAndamentos, lines)

        for dados in result:
            dadosTabela[title0].append(dados[0])
            dadosTabela[title1].append(dados[1])
            dadosTabela[title2].append(dados[2])
            dadosTabela[title3].append(dados[3])
            dadosTabela["status"].append(dados[4])

    print("\t\tBaixou Arquivos de Andamento")
    gerarArquivo.criarCSV(dadosTabela, parentDirectory+"/Detalhes andamento");
def pecorrerLinhasAndamentos(lines):

    colums = lines.find_all()
    colum0 = colums[0].text
    colum1 = colums[1].text
    colum2 = colums[2].text  # data
    colum3 = colums[3].find('a').get('href')  # link
    link = colum3
    #print("\t"+colum0, colum1, colum2, colum3)

    print("\t LINK:" + link);

    dados =  {"tipo":colum0,"descricao": colum1, "data":colum2, "link":link}
    # Criar uma pasta e arquivo json com dados
    file_dir = criarPastaJson(dados,directoryGlobal)
    print("----------"+ file_dir)

    #Verificar se tem link
    if link:
        statusDonwload = downloadArquivos.link(link, file_dir)
    else:
        print("\tLink não encontrado")
        statusDonwload = {'status Donwload': "Link não foi passado"}

    return [colum0,colum1,colum2,link,statusDonwload['status Donwload']]
    #Criar uma pasta para os downloads (se ela ainda não existir)
def pecorrerDocLicitacao(lines):

    colums = lines.find_all()
    colum0 = colums[0].text
    colum1 = colums[1].text
    colum2 = colums[2].text  # data
    colum3 = colums[3].find('a').get('href')  # link
    link = colum3
    '''
    colum0 =  re.sub(r"\s+", "", colum0)
    colum1 =  re.sub(r"\s+", "", colum1)
    colum2 =  re.sub(r"\s+", "", colum2)
    '''
    colum0 = colum0.replace("\n", "").strip()
    colum1 = colum1.replace("\n", "").strip()
    colum2 = colum2.replace("\n", "").strip()

    print("\t LINK:" + link);

    dados =  {"assunto":colum0,"tipo": colum1, "data":colum2, "link":link}
    # Criar uma pasta e arquivo json com dados
    file_dir = criarPastaJsonDOC(dados,directoryGlobal)


    #Verificar se tem link
    if link:
        statusDonwload = downloadArquivos.linkSemExtensao(link, file_dir)
    else:
        print("\tLink não encontrado")
        statusDonwload = {'status Donwload': "Link não foi passado"}

    return [colum0,colum1,colum2,statusDonwload['link_fuc'],statusDonwload['status Donwload']]
    #Criar uma pasta para os downloads (se ela ainda não existir)
def contratos(table,directory):
    print("\tAcessando contratos ligados a Licitação")

    # Criar uma pasta para os downloads (se ela ainda não existir)
    parentDirectory = directory
    directory = directory + "/Contratos"
    global directoryGlobalContratos
    directoryGlobalContratos = directory

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            print(f"A pasta '{directory}' já existe.")
    except Exception as e:
        print(f"\n\n\tErro ao criar a pasta '{directory}': {e} \n\n")

    lines = table.find_all("tr")
    linesTitle = lines[0].find_all("th")
    # Remover titulos das colunas
    lines.pop(0)

    if not lines:
        return []

    title0 = linesTitle[0].text
    title1 = linesTitle[1].text
    title2 = linesTitle[2].text
    title3 = linesTitle[3].text
    title4 = linesTitle[4].text
    title5 = linesTitle[5].text

    dadosTabela = {title0: [], title1: [], title2: [], title3: [], title4: [], title5: []}
    titles = [title0,title1,title2,title3,title4,title5]

    result = detalhesContrato.acessarPaginaDetalhes(lines,directory,titles,dadosTabela)

    gerarArquivo.criarCSV(result, parentDirectory+"/Contratos ligados a licitação");
def contratosVersaoJulho2024(soup,directory):
    listSacop = soup.select('.row:nth-child(6) .col-sm-12')
    listSacop = listSacop[0].find_all("a")
    lenListSacop = listSacop.__len__()

    if lenListSacop == 0:
        return [],

    # Criar uma pasta para os downloads (se ela ainda não existir)
    parentDirectory = directory
    directory = directory + "/Contratos"
    global directoryGlobalContratos
    directoryGlobalContratos = directory

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            print(f"A pasta '{directory}' já existe.")
    except Exception as e:
        print(f"\n\n\tErro ao criar a pasta '{directory}': {e} \n\n")

    linksSacop = listSacop
    result = detalhesContrato.acessarPaginaDetalhesNovaVersaoJulho2024(linksSacop,directory)
    gerarArquivo.criarCSV(result, parentDirectory+"/Contratos")
def runVerificarSeExisteTabelas(link,directory):

    from selenium.webdriver.chrome.options import Options
    if link:
        # Configurações para executar o Chrome em modo headless
        # Inicializa o driver do Selenium com as opções configuradas
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Ativa o modo headless
        driver = webdriver.Chrome(options=chrome_options)
        #driver = webdriver.Chrome()
        #driver.set_window_size(800, 600);
        driver.get(link)
        time.sleep(2)

        # Obter o código HTML da página
        html = driver.page_source
        # Analisar o HTML usando BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        # Navegar até a página
        verificarSeExisteTabelas(soup, directory)
        # Fechar o navegador
        driver.quit()

links = [
    #"https://transparencia.altoalegredomaranhao.ma.gov.br/licitacao/151640" #Tabela sem nada
    #"https://transparencia.altoalegredomaranhao.ma.gov.br/licitacao/172476", #Tabala com com um item
   #"https://transparencia.altoalegredomaranhao.ma.gov.br/licitacao/172444" #normal
   "https://transparencia.altoalegredomaranhao.ma.gov.br/licitacao/172450", #Normal com contratos
   #"https://transparencia.altoalegredomaranhao.ma.gov.br/licitacao/44042"  #Normal com apenas um contrato
          ]

for i in links:

    runVerificarSeExisteTabelas(i,"ARQUIVOS")

