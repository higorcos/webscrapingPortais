from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import os
from Licitacao_and_Contrato.licitacao import licitacaoPaginacao

# Registra o tempo de início
inicio = time.time()

linkLicitacao = "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/exibir";
nomePortal = "Mirador";
tipoPortal = "PM";

directoryInformation = {
    "mainFolder": "Downloads-" + nomePortal + "-" + tipoPortal + "",
    "licitacaoFolder": "licitacao",
}

# Criar uma pasta para os downloads (se ela ainda não existir)
if not os.path.exists(directoryInformation["mainFolder"]):
    os.makedirs(directoryInformation["mainFolder"])

# Criar uma nova instância do driver do Chrome
driver = webdriver.Chrome()

# Definir o tamanho da janela
driver.set_window_size(800, 600);


licitacaoPaginacao.traversev(driver,directoryInformation,linkLicitacao)

# fechar navegador
driver.quit()

# Registra o tempo de término
fim = time.time()

# Calcula o tempo total de execução
tempo_total = fim - inicio
print("\nTempo de execução",tempo_total)
