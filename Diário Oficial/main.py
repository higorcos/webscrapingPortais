from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
from Ultils import gerarArquivo,downloadArquivos



linkPortal = "https://transparencia.mirador.ma.gov.br/acessoInformacao/diario/diario";
nomePortal = "Mirador";
tipoPortal = "PM";
tipoArquivosDownloads = "Diário Oficial";

dadosTabela = {"Nº EDIÇÃO":[],"DATA":[], "STATUS":[], "LINK":[]}
# Criar uma pasta para os downloads (se ela ainda não existir)
download_dir = 'Downloads-'+nomePortal+'-'+tipoPortal+'-'+tipoArquivosDownloads;

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Criar uma nova instância do driver do Chrome
driver = webdriver.Chrome()

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
selectNumberPages = soup.select('#dtDiario_ellipsis+ .paginate_button a')
numberPages = int(selectNumberPages[0].text);
print(numberPages)


# Percorrer páginas
for i in range(96,numberPages):
    # Aguardar 1 segundo
    #time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Encontrar todas as tags
    colum0 = soup.find_all('td', {'class': 'sorting_2'});
    colum1 = soup.find_all('td', {'class': 'sorting_1'});
    colum2 = soup.select('.sorting_1 + .text-center');

    for line in range(0,colum0.__len__()):
        numberFile = colum0[line].text;
        dateFile = colum1[line].text;
        dateFileNewFormat = dateFile.replace('/','-') #remover barra


        # Obter o URL do atributo 'href' da tag <a>
        link_tag = colum2[line].find('a');
        link = link_tag.get('href')

        number0 = str(i)
        number0 += str(line)
        # Criar uma pasta individual para o arquivo baixado dentro da pasta de downloads
        newDir = "Nº " + numberFile + " DATA " + dateFileNewFormat + " " + number0
        file_dir = os.path.join(download_dir, newDir)

        # Verificar se encontrou a tag <a>
        if link:
            statusDonwload = downloadArquivos.link(link, file_dir)
        else:
            print("Link não encontrado")
            statusDonwload = {'status Donwload': "Link não foi passado"}

        print('Nº', numberFile, 'DATA:', dateFile, 'LINK:', link, 'Status', statusDonwload['status Donwload']);

        dadosTabela["Nº EDIÇÃO"].append(numberFile)
        dadosTabela["DATA"].append(dateFile)
        dadosTabela["STATUS"].append(statusDonwload['status Donwload'])
        dadosTabela["LINK"].append(link)


    if numberPages != i:
        button = driver.find_element(By.CSS_SELECTOR, "#dtDiario_next a");
        button.click();


gerarArquivo.CSV(dadosTabela,download_dir);
# Fechar o navegador
driver.quit()


