from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
from Ultils import gerarArquivo, downloadArquivos
from Licitacao_and_Contrato.contrato import detalhesContrato
import concurrent.futures

directoryGlobal = ''
globalParentDirectory = ''
def verificarSeExisteTabelas(soup,directory=''):
    tablesObj = {}

    #Encontrar Tabelas
        #-Licitantes
        #-Contratos vinculados
        #-Andamentos
    tables = soup.select('.col-xs-12')
    tablesLength = tables.__len__()

    #Não tem tabela
    if tablesLength == 0:
        return []
    #colocar em um objeto as tabelas encontradas
    for i in range(0,tablesLength):

        #Chave = Nome da tabela
        titleTable = tables[i].find_all("div", {"class": "panel-heading"})
        titleTable = titleTable[0].text

        #valores = dados da tabela
        bodyTable = tables[i]

        tablesObj[titleTable] = bodyTable

    #TIPO POSSIVEIS DE TABELAS EM DETALHES DE LICITAÇÃO
    if 'Andamentos' in tablesObj:
        print('\tPossui Atendimento')
        #andamentos(tablesObj['Andamentos'],directory)

    if 'Contratos vinculados' in tablesObj:
        print('\tPossui Contrato')
        contratos(tablesObj['Contratos vinculados'], directory)


    if 'Licitantes' in tablesObj:
        print('\tPossui Licitantes')
def andamentos(table,directory):
    print("\tDownload arquivos de andamento da Licitação")

    # Criar uma pasta para os downloads (se ela ainda não existir)
    parentDirectory = directory
    directory = directory+"/Andamento"
    global directoryGlobal
    directoryGlobal = directory

    if not os.path.exists(directory):
        os.makedirs(directory)

    lines = table.find_all("tr")
    linesTitle = lines[0].find_all("th")
    # Remover titulos das colunas
    lines.pop(0)

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

    print("\t-------Baixou Arquivos")
    gerarArquivo.criarCSV(dadosTabela, parentDirectory+"/Detalhes andamento");

def pecorrerLinhasAndamentos(lines):

    colums = lines.find_all()
    colum0 = colums[0].text
    colum1 = colums[1].text
    colum2 = colums[2].text  # data
    colum3 = colums[3].find('a').get('href')  # link
    link = colum3
    #print("\t"+colum0, colum1, colum2, colum3)

    print("\tLINK:" + colum3);

    # Criar uma pasta individual para o arquivo baixado dentro da pasta de downloads
    dateFileNewFormat = colum2.replace('/', '-').replace(':', '-')  # remover barra e dois pontos
    newDir = "TIPO " + colum0 + " " + dateFileNewFormat

    file_dir = os.path.join(directoryGlobal, newDir)

    # Verificar se tem link
    if link:
        statusDonwload = downloadArquivos.link(link, file_dir)
    else:
        print("\tLink não encontrado")
        statusDonwload = {'status Donwload': "Link não foi passado"}

    return [colum0,colum1,colum2,link,statusDonwload['status Donwload']]
    # Criar uma pasta para os downloads (se ela ainda não existir)
def contratos(table,directory):
    print("\tAcessando contratos ligados a Licitação")

    # Criar uma pasta para os downloads (se ela ainda não existir)
    parentDirectory = directory
    directory = directory + "/Contratos"
    global directoryGlobal
    directoryGlobal = directory

    if not os.path.exists(directory):
        os.makedirs(directory)

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

def runVerificarSeExisteTabelas(link,directory):

    from selenium.webdriver.chrome.options import Options

    # Configurações para executar o Chrome em modo headless
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Ativa o modo headless

    # Inicializa o driver do Selenium com as opções configuradas
    driver = webdriver.Chrome(options=chrome_options)


           # Criar uma nova instância do driver do Chrome
   # driver = webdriver.Chrome()
        # Definir o tamanho da janela
    driver.set_window_size(800, 600);
    driver.get(link)
           # Aguardar o carregamento da página
    #time.sleep(5)

        # Obter o código HTML da página
    html = driver.page_source
        # Analisar o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
        # Navegar até a página
    verificarSeExisteTabelas(soup, directory)
        # Fechar o navegador
    driver.quit()

'''
links = [
   "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/detalhes/991136437",
   "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/detalhes/991136424",
   "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/detalhes/991136513",
   "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/detalhes/140809"
          ]
for i in links:
    contratos(i)
'''
runVerificarSeExisteTabelas('https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/detalhes/991136498',"ARQUIVOS")