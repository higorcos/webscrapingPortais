from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import os
from Licitacao_Assesi.licitacao import licitacaoPaginacao
from selenium.webdriver.chrome.options import Options

# Registra o tempo de início
inicio = time.perf_counter()

linkLicitacao = "https://transparencia.altoalegredomaranhao.ma.gov.br/licitacoes";
nomePortal = "alto-alegre";
tipoPortal = "PM";

directoryInformation = {
    "mainFolder": "Downloads-" + nomePortal + "-" + tipoPortal + "",
    "licitacaoFolder": "licit",
}

# Criar uma pasta para os downloads (se ela ainda não existir)
if not os.path.exists(directoryInformation["mainFolder"]):
    os.makedirs(directoryInformation["mainFolder"])


# Configurações para executar o Chrome em modo headless
chrome_options = Options()
chrome_options.add_argument('--headless')  # Ativa o modo headless
#driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()
# Definir o tamanho da janela
#driver.set_window_size(800, 600);


licitacaoPaginacao.traversev(driver,directoryInformation,linkLicitacao)

# fechar navegador
driver.quit()

# Registra o tempo de término
fim = time.time()


fim = time.perf_counter()
tempo_total = fim - inicio

print("tempo de execução", tempo_total)