from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from Licitacao_and_Contrato.licitacao import detalhesLicitacao



def traversev(driver,directoryInformation,link):

    #acessar link
    driver.get(link)

    # Aguardar o carregamento da página
    time.sleep(8)

    # Obter o código HTML da página
    html = driver.page_source

    # Analisar o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    #numero de paginas
    selectNumberPages = soup.select('#dtLicitacoes_ellipsis+ .paginate_button a')
    numberPages = int(selectNumberPages[0].text)

    linksPagesDetails = []


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
            linksPagesDetails.append(link.get('href'))

        if numberPages != i:
            button = driver.find_element(By.CSS_SELECTOR, "#dtLicitacoes_next a");
            button.click();


    #print(linkPagesDetails.__len__())

    for linkPage in linksPagesDetails:
        #print("Licitação Acessada",linkPage)

        # abrir uma nova aba
        driver.execute_script("window.open('about:blank', '_blank');")

        # Captura as alças das guias
        janelas = driver.window_handles

        # Troca o foco para a nova aba (a última na lista de alças)
        driver.switch_to.window(janelas[-1])

        # Função que irá cuidar do detalhes da licitação (passando a URL)
        detalhesLicitacao.mostrarDetalhe(driver,directoryInformation,linkPage)

        # Feche a aba atual
        driver.close()
        # Troca o foco para a nova aba (a última na lista de alças)
        driver.switch_to.window(janelas[0])
    return []

def run_traversev():
    '''
    linkLicitacao = "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/exibir";
    nomePortal = "TESTE";
    tipoPortal = "TESTE";


    directoryInformation = {
       "mainFolder": "Downloads-" + nomePortal + "-" + tipoPortal + "",
       "licitacaoFolder": "BBBBB",
    }
    # Criar uma nova instância do driver do Chrome
    driver = webdriver.Chrome()

    # Definir o tamanho da janela
    driver.set_window_size(800, 600);

    traversev(driver, directoryInformation, linkLicitacao)

    # fechar navegador
    driver.quit()
    '''
run_traversev()
