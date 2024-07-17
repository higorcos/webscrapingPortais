from selenium import webdriver
import time
from Licitacao_Siganet.licitacao import licitacaoPaginacao
from selenium.webdriver.chrome.options import Options

# Registra o tempo de início
inicio = time.perf_counter()

#linkLicitacao = "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/exibir";
linkLicitacao = "https://transparencia.parnarama.ma.gov.br/acessoInformacao/licitacao/tce"
nomePortal = "Parnarama";
tipoPortal = "PM";

directoryInformation = {
    "mainFolder": "Downloads-" + nomePortal + "-" + tipoPortal + "",
    "licitacaoFolder": "parnarama-lici",
}

# Criar uma pasta para os downloads (se ela ainda não existir)
'''
if not os.path.exists(directoryInformation["mainFolder"]):
    os.makedirs(directoryInformation["mainFolder"])
'''

# Configurações para executar o Chrome em modo headless
chrome_options = Options()
chrome_options.add_argument('--headless')  # Ativa o modo headless
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome()
# Definir o tamanho da janela
driver.set_window_size(800, 600);


licitacaoPaginacao.janela(driver,directoryInformation,linkLicitacao)

# fechar navegador
driver.quit()

# Registra o tempo de término
fim = time.time()


fim = time.perf_counter()
tempo_total = fim - inicio

print("tempo de execução", tempo_total)