from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import os

linkPortal = "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/exibir";
nomePortal = "Mirador";
tipoPortal = "PM";
tipoArquivosDownloads = "Licitações";

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

#numero de paginas
selectNumberPages = soup.select('#dtLicitacoes_ellipsis+ .paginate_button a')
numberPages = int(selectNumberPages[0].text)
print(numberPages)

linkPagesDetails = []


# Percorrer páginas
for i in range(0,numberPages):
    # Aguardar 1 segundo
    #time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    #Pegar os links da paginação (array com varios links)
    currentPageLinks = soup.select('#dtLicitacoes a')

    #adicionar cada link no array (adicionar apenas o link)
    for link in currentPageLinks:
        linkPagesDetails.append(link.get('href'))

    if numberPages != i:
        button = driver.find_element(By.CSS_SELECTOR, "#dtLicitacoes_next a");
        button.click();

# Fechar o navegador
print(linkPagesDetails.__len__())

for newpage in linkPagesDetails:
    print(newpage)

    # abrir uma nova aba
    driver.execute_script("window.open('about:blank', '_blank');")

    # Captura as alças das guias
    janelas = driver.window_handles

    # Troca o foco para a nova aba (a última na lista de alças)
    driver.switch_to.window(janelas[-1])

    # Agora você está na nova aba e pode navegar para um URL específico
    driver.get(newpage)

    # Feche a aba atual
    driver.close()
    # Troca o foco para a nova aba (a última na lista de alças)
    driver.switch_to.window(janelas[0])

#fechar navegador
driver.quit()
