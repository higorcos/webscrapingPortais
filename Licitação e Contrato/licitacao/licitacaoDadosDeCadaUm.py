from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import os

linkPortal = "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/detalhes/991136499";
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
time.sleep(1)

# Obter o código HTML da página
html = driver.page_source

# Analisar o HTML usando BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

#Informações das licitações
selectDivs = soup.select('.form-group')

for input in selectDivs:

    if (input.find("input")):
        print("Chave:", input.find("label").text)
        print("Valor: ",input.find("input")["value"])
    else:
        print("")
##Dados que não seguem o mesmo padrão no HTML
    #Natureza de despesa:
    #Objeto:
naturezaDespesa = soup.select('.col-md-2+ .col-md-12')
objeto = soup.select('.col-md-4+ .col-md-12')

print(naturezaDespesa[0].find("label").text, naturezaDespesa[0].find("textarea").text)
print(objeto[0].find("label").text, objeto[0].find("textarea").text)

# Fechar o navegador
driver.quit()




