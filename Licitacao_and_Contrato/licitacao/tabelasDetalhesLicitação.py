from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
from Ultils import gerarArquivo, downloadArquivos
import concurrent.futures

directoryGlobal = ''
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
        #print('\tPossui Atendimento')
        andamentos(tablesObj['Andamentos'],directory)

    if 'Contratos vinculados' in tablesObj:
        print('\tPossui Contrato')

    if 'Licitantes' in tablesObj:
        print('\tPossui Licitantes')

    return []

def andamentos(table,directory):
    print("\tDownload arquivos de andamento da Licitação")

    # Criar uma pasta para os downloads (se ela ainda não existir)
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

    print("\n\t\t"+__name__+"\n")
    #if __name__ == "__main__":

    #print("\t--------------",directoryGlobal)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        cods = executor.map(pecorrerLinhasAndamentos, lines)
    print("\t-------Baixou Arquivos")

    #sequencial
    #for i in range(0, lines.__len__()):
        #pecorrerLinhasAndamentos(lines[i])
    #gerarArquivo.criarCSV(dadosTabela, directory);

def pecorrerLinhasAndamentos(lines):

    colums = lines.find_all()
    colum0 = colums[0].text
    colum1 = colums[1].text
    colum2 = colums[2].text  # data
    colum3 = colums[3].find('a').get('href')  # link
    link = colum3

    #print("\t"+colum0, colum1, colum2, colum3)
    # print("\tTIPO: " +  colum0 );

    print("\tLINK:" + colum3);

    # Criar uma pasta individual para o arquivo baixado dentro da pasta de downloads
    number0 = '0'
    dateFileNewFormat = colum2.replace('/', '-').replace(':', '-')  # remover barra e dois pontos
    # newDir = "TIPO " +  colum0 + " DESCRICAO " +  colum1 + " DATA "+dateFileNewFormat + "" +number0
    #newDir = "TIPO " + colum0 + " " + number0
    newDir = "TIPO " + colum0 + " " + dateFileNewFormat

    file_dir = os.path.join(directoryGlobal, newDir)
    # time.sleep(1)

    # Verificar se encontrou a tag <a>
    if link:
        statusDonwload = downloadArquivos.link(link, file_dir)
    else:
        print("\tLink não encontrado")
        statusDonwload = {'status Donwload': "Link não foi passado"}

    # print("\tTIPO: " +  colum0 + " DESCRICAO: " +  colum1 + " DATA ENVIO: " +colum2 + " LINK: "+ colum3 + ' Status: ', statusDonwload['status Donwload']);
    # print("\tTIPO: " +  colum0 + ' Status: ', statusDonwload['status Donwload']);

    '''
    dadosTabela[title0].append(colum0)
    dadosTabela[title1].append(colum1)
    dadosTabela[title2].append(colum2)
    dadosTabela[title3].append(colum3)
    dadosTabela["status"].append(statusDonwload['status Donwload'])
    # dadosTabela["status"].append("ERRO")
    '''

def contratos(link):

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
    verificarSeExisteTabelas(soup)
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
#contratos('https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/detalhes/991136499')