from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from bs4 import BeautifulSoup
import time
import os
from Ultils import gerarArquivo,downloadArquivos
from Ultils.pastas import pastasDocumentosDosModulos
import concurrent.futures
from selenium.webdriver.chrome.options import Options
from Ultils.pastas.pastasDocumentosDosModulos import diarioTECUPDATE as criarPastaJson



linkPortal = "https://tecnologiaupdate.com/pirapemas.diario/showAllEditions.php";
nomePortal = "Pirapemas";
tipoPortal = "PM";
tipoArquivosDownloads = "Diario";

dadosTabela = {}
dados = {}
# Criar uma pasta para os downloads (se ela ainda não existir)
download_dir = 'Downloads-'+nomePortal+'-'+tipoPortal+'-'+tipoArquivosDownloads;

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Criar uma nova instância do driver do Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Ativa o modo headless
driver = webdriver.Chrome(options=chrome_options)

# Definir o tamanho da janela
driver.set_window_size(800, 1000);
# Navegar até a página
driver.get(linkPortal)

# Aguardar o carregamento da página
time.sleep(2)

# Obter o código HTML da página
html = driver.page_source

# Analisar o HTML usando BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

table = soup.select('.editionsTable')
titleTable = table[0].find_all('th')
lines = table[0].find_all('tr')
lines.pop(0)

title0 = titleTable[0].text
title1 = titleTable[1].text
title2 = titleTable[2].text

dadosTabela[title0] = []
dadosTabela[title1] = []
dadosTabela[title2] = []
dadosTabela["link"] = []
dadosTabela["status"] = []
dadosTabela["pasta"] = []


def converter_data(texto_data):
    # Dicionário para mapear os nomes dos dias da semana em português para inglês
    dias_semana = {
        "segunda": "Monday",
        "terça": "Tuesday",
        "ter�a": "Tuesday",
        "quarta": "Wednesday",
        "quinta": "Thursday",
        "sexta": "Friday",
        "sábado": "Saturday",
        "s�bado": "Saturday",
        "sçbado": "Saturday",
        "domingo": "Sunday"
    }

    # Dicionário para mapear os nomes dos meses em português para inglês
    meses = {
        "janeiro": "January",
        "fevereiro": "February",
        "março": "March",
        "mar�o": "March",
        "abril": "April",
        "maio": "May",
        "junho": "June",
        "julho": "July",
        "agosto": "August",
        "setembro": "September",
        "outubro": "October",
        "novembro": "November",
        "dezembro": "December"
    }

    # Substituindo os nomes dos dias da semana em português pelos equivalentes em inglês
    for dia_pt, dia_en in dias_semana.items():
        texto_data = texto_data.replace(dia_pt, dia_en)

    # Substituindo os nomes dos meses em português pelos equivalentes em inglês
    for mes_pt, mes_en in meses.items():
        texto_data = texto_data.replace(mes_pt, mes_en)

    # Convertendo para objeto datetime
    data = datetime.strptime(texto_data, "%A %d %B %Y")

    # Formatando a data para o formato desejado
    data_formatada = data.strftime("%d/%m/%Y")

    return data_formatada
def tem_letras(string):
    return bool(re.search('[a-zA-Z]', string))

print("\n\n\t\t"
      "Recomendações\n"
"\t- não mexer no terminal\n"
"\t- adicionar o executável a uma pasta para os arquivos gerados ficarem dentro\n"
"\t- no arquivo .csv ficaram o status de cada arquivo e informações assim como dentro de casa pasta\n"
"\t- se você interromper o executável. Rode novamente mas antes delete a pasta de downloads \n\n")

print("Quantidade de Diários: ",lines.__len__())
for i in range(0, lines.__len__()):

    line = lines[i].find_all('td')
    dado0 = line[0].text
    dado1 = line[1].text
    dado1 = dado1.replace("�","ç")
    dado2 = line[2].text

    tituloDiario = dado0

    ##FORMATAR DATA
    # Convertendo para objeto datetime
    date = converter_data(dado1)

    linkDownload='https://tecnologiaupdate.com/pirapemas.diario/utils/showPublication.php?filename='+tituloDiario+'.pdf'
    linkDownloadViews='https://tecnologiaupdate.com/pirapemas.diario/utils/showPublication.php?filename='+tituloDiario+'.pdff&mode=1'

    dados = {"edicao": dado0, "data": date, "tipo": dado2, "link": linkDownload , 'id': i}
    # Criar uma pasta e arquivo json com dados
    file_dir = criarPastaJson(dados, download_dir)

    # Verificar se tem link
    if linkDownload:
        statusDonwload = downloadArquivos.link(linkDownload, file_dir)
    else:
        print("\tLink não encontrado")
        statusDonwload = {'status Donwload': "Link não foi passado"}

    dadosTabela[title0].append(dado0)
    dadosTabela[title1].append(date)
    dadosTabela[title2].append(dado2)
    dadosTabela['status'].append(statusDonwload['status Donwload'])
    dadosTabela['pasta'].append(file_dir)
    dadosTabela['link'].append(linkDownloadViews)

gerarArquivo.criarCSV(dadosTabela, download_dir);
driver.quit()
print('\n\tFIM')
