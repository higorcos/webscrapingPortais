from selenium.webdriver.chrome.options import Options
from Ultils import gerarArquivo,downloadArquivos
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import concurrent.futures
import time
import os


def pecorrerLinhas(row):
    if not row:  # Verifica se a linha está vazia
        print('------')
        return ['', '', '', '']

    print(f"{row} - {time.strftime('%X')}")
    numberFile = row[0]
    dateFile = row[1]
    dateFileNewFormat = dateFile.replace('/', '-')  # remover barra
    link = row[3]

    number0 = str(i)
    # Criar uma pasta individual para o arquivo baixado dentro da pasta de downloads
    newDir = "Nº " + numberFile + " DATA " + dateFileNewFormat
    file_dir = os.path.join(download_dir, newDir)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # Verificar se encontrou a tag <a>
    if link:
        statusDownload = downloadArquivos.link(link, file_dir)
    else:
        print("Link não encontrado")
        statusDownload = {'status Donwload': "Link não foi informado"}

    return [numberFile,dateFile,statusDownload['status Donwload'],link]

linkPortal = "https://parnarama.diariooficialmunicipal.com/?p=edicao";
dnsPortal = "https://parnarama.diariooficialmunicipal.com/"
nomePortal = "Parnarama";
tipoPortal = "PM";
tipoArquivosDownloads = "Diario";

dadosTabela = {"Nº EDIÇÃO":[],"DATA":[], "STATUS":[], "LINK":[]}
# Criar uma pasta para os downloads (se ela ainda não existir)
download_dir = tipoArquivosDownloads+"-"+nomePortal+'-'+tipoPortal;

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

chrome_options = Options()
chrome_options.add_argument('--headless')  # Ativa o modo headless
driver = webdriver.Chrome(options=chrome_options)

# Definir o tamanho da janela
driver.set_window_size(800, 600);
# Navegar até a página
driver.get(linkPortal)

# Aguardar o carregamento da página
time.sleep(5)

# Obter o código HTML da página
html = driver.page_source

# Analisar o HTML usando BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# #numero de paginas
selectNumberPages = soup.select('.page-last a')
numberPages = int(selectNumberPages[0].text);
print(numberPages)


# Percorrer páginas
for i in range(0,numberPages):
    # Aguardar 1 segundo
    #time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Encontrar todas as tags
    table = soup.select('#table-data-edicao')
    rows = table[0].find_all('tr');
    all_rows = []
    # Iterar sobre as linhas e pegar todas as células de cada linha
    for row in rows:
        cells = row.find_all('td')
        cell_contents = []
        for cell in cells:
            a_tag = cell.find('a')
            if a_tag and 'href' in a_tag.attrs:
                cell_contents.append(dnsPortal+a_tag['href'])
            else:
                cell_contents.append(cell.get_text(strip=True))
        all_rows.append(cell_contents)

        print('Antes')

    with concurrent.futures.ThreadPoolExecutor(6) as executor:
        result = executor.map(pecorrerLinhas, all_rows)

    for dados in result:
        dadosTabela["Nº EDIÇÃO"].append(dados[0])
        dadosTabela["DATA"].append(dados[1])
        dadosTabela["STATUS"].append(dados[2])
        dadosTabela["LINK"].append(dados[3])
    print('Depois')



    if numberPages != i:
        button = driver.find_element(By.CSS_SELECTOR, ".page-next a");
        button.click();
        print('Mudou')

gerarArquivo.criarCSV(dadosTabela, download_dir);
# Fechar o navegador
driver.quit()