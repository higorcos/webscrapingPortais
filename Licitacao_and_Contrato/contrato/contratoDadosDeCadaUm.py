from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
from Ultils import gerarArquivo

linkPortal = "https://transparencia.balsas.ma.gov.br/acessoInformacao/contratos/contratos/detalhes/113748";
nomePortal = "Mirador";
tipoPortal = "PM";
tipoArquivosDownloads = "Licitações";
# Caminho do arquivo CSV
caminho_arquivo = ""+tipoArquivosDownloads+".csv"

data={}
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
    if (input.find("label")):
        if (input.find("input")):
            print("Chave:",input.find("label").text)
            print("Valor: ",input.find("input")["value"])
            value = input.find("input")["value"]
            chave = input.find("label").text

            #salvando
            data[chave] = []
            data[chave].append(value)
        else:
            print("")
    else:
        print('\nElemento diferente de um input')

##Dados que não seguem o mesmo padrão no HTML
    #Objeto:
objeto = soup.select('.col-md-12:nth-child(11)')

value = objeto[0].find("textarea").text
chave = objeto[0].find("label").text

data[chave] = []
data[chave].append(value)

#Criar tabela
gerarArquivo.criarCSV(data, 'detalhes da licitação')
# Fechar o navegador
driver.quit()




