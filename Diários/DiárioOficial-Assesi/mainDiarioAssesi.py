from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
from Ultils import gerarArquivo, downloadArquivos
from Ultils.pastas import pastasDocumentosDosModulos
import concurrent.futures
from selenium.webdriver.chrome.options import Options

linkPortal = "https://transparencia.altoalegredomaranhao.ma.gov.br/diario";
nomePortal = "alto-alegre-do-maranhao";
tipoPortal = "";
tipoArquivosDownloads = "Diario";

dadosTabela = {}
# Criar uma pasta para os downloads (se ela ainda não existir)
download_dir = 'Downloads-' + nomePortal + '-' + tipoPortal + '-' + tipoArquivosDownloads;

if not os.path.exists(download_dir):
    os.makedirs(download_dir)


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'

# Criar uma nova instância do driver do Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Ativa o modo headless
chrome_options.add_argument(f'user-agent={user_agent}')  # Ativa o modo headless
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome()


# Definir o tamanho da janela
driver.set_window_size(800, 600);
# Navegar até a página
driver.get(linkPortal)

# Aguardar o carregamento da página
time.sleep(2)

# Obter o código HTML da página
html = driver.page_source

# Acessar lista tabelas de diário
button = driver.find_element(By.CSS_SELECTOR, ".nav-item:nth-child(5) .nav-link")
button.click()

# Analisar o HTML usando BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

table = soup.select('#tableLicitacoes_wrapper')
selectNumberPages = soup.select('#tableLicitacoes_ellipsis+ .page-item .page-link')

numberPages = int(selectNumberPages[0].text)
print(numberPages)
titleTable = table[0].find_all('th')

title0 = titleTable[0].text
title1 = titleTable[1].text
title2 = titleTable[2].text
title3 = titleTable[3].text

dadosTabela[title0] = []
dadosTabela[title1] = []
dadosTabela[title2] = []
dadosTabela[title3] = []
dadosTabela["status"] = []
dadosTabela["pasta"] = []


def processarLinha(line):
    lines = line.find_all('td')

    colum0 = lines[0].text
    colum1 = lines[1].text
    colum2 = lines[2].text
    colum3 = lines[3]

    if colum3.find('a'):
        if colum3.find('a').get('href'):
            link = colum3.find('a').get('href')
        else:
            link = ''
    else:
        link = ''

    print(link)

    # Verificar se tem link
    if link and link != '':

        id = os.path.basename(link)

        # Criar uma pasta individual para o arquivo baixado dentro da pasta de downloads
        dados = {"Publicação": colum0.strip(), "Data": colum1.strip(), "Tipo Publicação": colum2.strip(), "Link": link,
                 "ID": ""}
        file_dir = pastasDocumentosDosModulos.diarioWEBSERVER(dados, gDiretory)

        statusDonwload = downloadArquivos.linkSemExtensao(link, file_dir)
    else:
        print("Link não encontrado")
        statusDonwload = {'status Donwload': "Link não foi passado"}

    return [colum0.strip(), colum1.strip(), colum2.strip(), link, statusDonwload['status Donwload'], file_dir]

# Percorrer páginas da primeira tabela
def percorrerPaginasPrimeiraTabela():
    for i in range(0, numberPages):
        # Aguardar 1 segundo
        # time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        table = soup.select('#tableLicitacoes_wrapper')
        selectNumberPages = soup.select('#tableLicitacoes_ellipsis+ .page-item .page-link')

        titleTable = table[0].find_all('th')

        colums = table[0].find_all('tr')
        colums.pop(0)

        global gDiretory
        gDiretory = download_dir

        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = executor.map(processarLinha, colums)

            for dados in result:
                dadosTabela[title0].append(dados[0])
                dadosTabela[title1].append(dados[1])
                dadosTabela[title2].append(dados[2])
                dadosTabela[title3].append(dados[3])
                dadosTabela["status"].append(dados[4])
                dadosTabela["pasta"].append(dados[5])

        if numberPages - 1 != i:
            print('Proximo')
            buttonNext = driver.find_element(By.XPATH, '//*[@id="tableLicitacoes_next"]/a')
            buttonNext.click()

def processarLinhaSegundaTabela(line):
    lines = line.find_all('td')

    colum0 = lines[0].text
    colum1 = lines[1].text
    colum2 = lines[3].text
    colum3 = lines[4]

    if colum3.find('a'):
        if colum3.find('a').get('href'):
            link = colum3.find('a').get('href')
        else:
            link = ''
    else:
        link = ''

    print(link)

    # Verificar se tem link
    if link and link != '':

        id = os.path.basename(link)

        # Criar uma pasta individual para o arquivo baixado dentro da pasta de downloads
        dados = {"Publicação": colum0.strip(), "Data": colum1.strip(), "Tipo Publicação": colum2.strip(), "Link": link,
                 "ID": ""}
        file_dir = pastasDocumentosDosModulos.diarioWEBSERVER(dados, gDiretory2)

        statusDonwload = downloadArquivos.linkSemExtensao(link, file_dir)
    else:
        print("Link não encontrado")
        statusDonwload = {'status Donwload': "Link não foi passado"}

    return [colum0.strip(), colum1.strip(), colum2.strip(), link, statusDonwload['status Donwload'], file_dir]

def percorrerPaginasSegundaTabela():
    html2 = driver.page_source
    soup2 = BeautifulSoup(html2, "html.parser")
    table02 = soup2.select('#tableLicitacoess')

    if table02:
        colums = table02[0].find_all('tr')
        colums.pop(0)

        global gDiretory2
        gDiretory2 = download_dir

        with concurrent.futures.ThreadPoolExecutor() as executor:
            result2 = executor.map(processarLinhaSegundaTabela, colums)

            for dadosPg in result2:
                dadosTabela[title0].append(dadosPg[0])
                dadosTabela[title1].append(dadosPg[1])
                dadosTabela[title2].append(dadosPg[2])
                dadosTabela[title3].append(dadosPg[3])
                dadosTabela["status"].append(dadosPg[4])
                dadosTabela["pasta"].append(dadosPg[5])

        #Verificar botão de proxima página
        buttonNext = driver.find_element(By.ID,'tableLicitacoess_next')

        botaoHTML = soup2.select("#tableLicitacoess_next")

        print(botaoHTML)

        # Verificar se o botão está desabilitado
        if botaoHTML[0] and "disabled" in botaoHTML[0].get("class", []):
            print("")
        else:
            if buttonNext:
                buttonNext.click()
                percorrerPaginasSegundaTabela()

def main():
    percorrerPaginasPrimeiraTabela()
    percorrerPaginasSegundaTabela()
    gerarArquivo.criarCSV(dadosTabela, download_dir);
    # Fechar o navegador
    driver.quit()



main()


