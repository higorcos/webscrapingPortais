from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
import time
import os
from selenium.webdriver.common.by import By
from ePCA import tela02 as segundaTela
from ePCA.Model import cidadeAnoSatus as SQLcidadeAnoStatus
from ePCA.Model import cidade as SQLcidade
from ePCA.Model import ano as SQLano
from ePCA.Model import db as DB
import numpy as np
import concurrent.futures


def acessarPaginaPrincipal():
    diretorio = criarDiretorioDeDownload()

    link = "https://app2.tcema.tc.br/PCA/visualizarestrutura.zul"
    # Iniciar Chrome
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": diretorio,  # Altere para o caminho desejado
        "download.prompt_for_download": False,  # Impedir pop-up de download
        "download.directory_upgrade": True,  # Garantir que o diretório é atualizado
        "safebrowsing.enabled": True  # Habilitar navegação segura
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Inicializar o ChromeDriver com as opções
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(2000, 800);
    #driver.set_window_size(800, 1000);
    driver.get(link)
    time.sleep(5) #delay

    #conexao Banco De Dados
    conexaoDB = DB.create_connection()
    botaoMostrarCidade(driver)
    resultadoQuantidadeDeNomeDeCidadeNoLayout = quantidadeDeNomeDeCidadeNoLayout(driver)
    quantidadePaginacao = int(quantidadePaginacaoCidade(driver))

    for paginaCidade in range(quantidadePaginacao):
        if paginaCidade != 0:
            print(paginaCidade)
            sairEvoltarParaPaginaPrincipal(driver)
            botaoMostrarCidade(driver)
            for k in range(paginaCidade):
                avancarListaCidades(driver)

        for posicaoNomeNaLista in range(resultadoQuantidadeDeNomeDeCidadeNoLayout):
            posicaoElemento = posicaoNomeNaLista+1
            if posicaoElemento != 1:
                botaoMostrarCidade(driver)

            cidadeSelecionada = clickSelecaoCidade(driver,posicaoElemento)
            #cidadeSelecionada = clickSelecaoCidade(driver,2)
            idCidade = SQLcidade.inserir_cidade(conexaoDB,cidadeSelecionada)


            ##ANO
            time.sleep(0.5)  # delay
            botaoMostrarAnos(driver)
            resultadoQuantidadeDeAnosNoLayout = quantidadeDeAnosNoLayout(driver)
            arraySequencial = np.arange(1, resultadoQuantidadeDeAnosNoLayout + 1)

            parametros = [(paginaCidade + 1, posicaoNomeNaLista + 1, int(num)) for num in arraySequencial]


            with concurrent.futures.ThreadPoolExecutor() as executor:
                result = executor.map(novaJanelaParaExecutar, parametros)

            posicaoCidadeNaPaginacao = paginaCidade + 1
            ondemDaCidadeNoLayout = posicaoNomeNaLista + 1

            #Abrir umas noba aba e fechar a atinga e rodar
            sairEvoltarParaPaginaPrincipal(driver)
            pecorrerAteCidadeNovamente(driver, posicaoCidadeNaPaginacao, ondemDaCidadeNoLayout)

            '''
            for param in parametros:
                print(param)
            '''
            '''
            for j in range(resultadoQuantidadeDeAnosNoLayout):
                posicaoElementoAno = j + 1
                if posicaoElementoAno != 1:
                    time.sleep(0.7)  # delay
                    botaoMostrarAnos(driver)

                anoSelecionado = clickSelecaoDoAno(driver,posicaoElementoAno)
                idAno = SQLano.inserir_ano(conexaoDB,anoSelecionado)
                valoresCidadeAnoStatus = [idCidade,idAno]

                verificarSeExisteEjaFinalizado = SQLcidadeAnoStatus.cidadeAnoStatus_existeStatus(conexaoDB,valoresCidadeAnoStatus)
                if verificarSeExisteEjaFinalizado:
                    continue
                else:

                    idCidadeAnoStatus = SQLcidadeAnoStatus.inserir_cidadeAnoStatus(conexaoDB,valoresCidadeAnoStatus)
                    
                    resultadoVerificacaoExistencia = verificarEclickDeEnviar(driver,conexaoDB,idCidadeAnoStatus);

                    if not resultadoVerificacaoExistencia:
                        print('Não Possui a informação')
                    else:
                        segundaTela.acessarSegundaTela(driver,diretorio)
                        sairEvoltarParaPaginaPrincipal(driver)
                    
            '''



    #botaoMostrarAnos(driver)
    #clickSelecaoDoAno(driver)

    #time.sleep(10)
    #driver.quit()
def botaoMostrarCidade(driver):
    buttonAcessarNomeCidade = driver.find_element(By.XPATH,'/html/body/div/div[4]/div[2]/div/div/div/div[1]/div/div[2]/div[1]/span[2]/a')
    buttonAcessarNomeCidade.click()
    time.sleep(0.5)
    return
def quantidadePaginacaoCidade(driver):
    buttonParaAvancarNomeDasCidades = driver.find_element(By.XPATH,'/html/body/div[2]/div/table/tbody/tr/td/table/tbody/tr/td/div/div[1]/div/ul/li[3]/span')
    value = buttonParaAvancarNomeDasCidades.text
    return value.replace(" ", "").replace("/", "")
def avancarListaCidades(driver):
    buttonParaAvancarNomeDasCidades = driver.find_element(By.XPATH, '/html/body/div[2]/div/table/tbody/tr/td/table/tbody/tr/td/div/div[1]/div/ul/li[4]/a')
    buttonParaAvancarNomeDasCidades.click()
    time.sleep(0.2)
def quantidadeDeNomeDeCidadeNoLayout(driver):
    soup = transformarDriveEmTextoHtml(driver)
    # Pegando o numero de cidades que é mostrado na listagem
    listNames = soup.select('.z-bandbox-popup')
    listNames = listNames[0].find_all('td', 'z-listcell')
    #print('\t N° op cidades: ',listNames.__len__())

    return listNames.__len__()
def clickSelecaoCidade(driver,posicaoElemento):
    # xpath Primeiro - '/html/body/div[2]/div/table/tbody/tr/td/table/tbody/tr/td/div/div[4]/table/tbody[1]/tr[1]/td/div'
    # xpath ultimo - '/html/body/div[2]/div/table/tbody/tr/td/table/tbody/tr/td/div/div[4]/table/tbody[1]/tr[5]/td/div'
    xPath = f'/html/body/div[2]/div/table/tbody/tr/td/table/tbody/tr/td/div/div[4]/table/tbody[1]/tr[{str(posicaoElemento)}]/td/div'
    selecionarNomeEspecificoDeUmaCidade = driver.find_element(By.XPATH,xPath)
    cidadeSelecionada = selecionarNomeEspecificoDeUmaCidade.text
    selecionarNomeEspecificoDeUmaCidade.click()
    time.sleep(0.7)
    #print('\t Cidade Selecionada: ',cidadeSelecionada)
    return [cidadeSelecionada]
def quantidadeDeAnosNoLayout(driver):
    soup = transformarDriveEmTextoHtml(driver)
    listaAnos = soup.select('.z-combobox-content')  # Anos
    listaAnos = listaAnos[0].find_all('span', 'z-comboitem-text')
    time.sleep(0.7)
    return listaAnos.__len__()
def clickSelecaoDoAno(driver,posicaoElemento):
    valueSelecao = f"/html/body/div[2]/ul/li[{str(posicaoElemento)}]"
    selecionarAno = driver.find_element(By.XPATH, valueSelecao)
    anoSelecionado = selecionarAno.text
    selecionarAno.click()
    time.sleep(0.7)
    #print("Ano Selecionado", anoSelecionado)
    return [anoSelecionado]
def botaoMostrarAnos(driver):
    mostrarAnos = driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[2]/div/div/div/div[1]/div/div[2]/div[2]/span[2]/a')
    mostrarAnos.click()
    time.sleep(0.3)
    return
def verificarEclickDeEnviar(driver,conexaoDB,id):
    #Antes de enviar verificar se o nome tem arquivo
    time.sleep(0.7)
    inputComStatusDoAno = driver.find_element(By.XPATH,'/html/body/div/div[4]/div[2]/div/div/div/div[1]/div/div[2]/div[3]/table[1]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/input')
    inputComStatusDoAno = inputComStatusDoAno.get_attribute('value')

    if "Não validada" in inputComStatusDoAno:
        print('NÃO VALIDADA')
        id = ["sem arquivos",id]
        SQLcidadeAnoStatus.update_cidadesAnoStatus(conexaoDB,id)
        return False

    time.sleep(0.2)
    buttonEnviar = driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[2]/div/div/div/div[1]/div/div[2]/table/tbody/tr/td/table/tbody/tr/td/div/button')
    buttonEnviar.click()
    time.sleep(0.3)
    return True
def transformarDriveEmTextoHtml(driver):
    # Obter o código HTML da página
    html = driver.page_source
    # Analisar o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return soup
def sairEvoltarParaPaginaPrincipal(driver):
    sair = driver.find_element(By.XPATH,'/html/body/div/div[4]/div[1]/div[1]/div/div/div[3]/table/tbody/tr/td/table/tbody/tr/td[17]/button')
    sair.click()
    time.sleep(0.6)
    driver.back()
    time.sleep(0.4)
    return
def criarDiretorioDeDownload():
    import os

    # Obter o diretório atual do script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Criar uma pasta de downloads dentro do diretório atual
    download_directory = os.path.join(current_directory, "downloads")
    os.makedirs(download_directory, exist_ok=True)

    return download_directory
def pecorrerAteCidadeNovamente(driver,posicaoCidadeNaPaginacao,ondemDaCidadeNoLayout):
    botaoMostrarCidade(driver)
    if posicaoCidadeNaPaginacao != 1:
        for k in range(posicaoCidadeNaPaginacao):
            avancarListaCidades(driver)
    cidadeSelecionada = clickSelecaoCidade(driver, ondemDaCidadeNoLayout)
def novaJanelaParaExecutar(parametros):
    diretorio = criarDiretorioDeDownload()
    link = "https://app2.tcema.tc.br/PCA/visualizarestrutura.zul"
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": diretorio,  # Altere para o caminho desejado
        "download.prompt_for_download": False,  # Impedir pop-up de download
        "download.directory_upgrade": True,  # Garantir que o diretório é atualizado
        "safebrowsing.enabled": True  # Habilitar navegação segura
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Inicializar o ChromeDriver com as opções
    driver = webdriver.Chrome(options=chrome_options)
    #driver.set_window_size(2000, 800);
    driver.set_window_size(800, 1000);
    driver.get(link)
    time.sleep(5)  # delay


    posicaoCidadeNaPaginacao, ondemDaCidadeNoLayout, posicaoAnoNoLayout = parametros


    sairEvoltarParaPaginaPrincipal(driver)
    pecorrerAteCidadeNovamente(driver, posicaoCidadeNaPaginacao, ondemDaCidadeNoLayout)
    botaoMostrarAnos(driver)
    anoSelecionado = clickSelecaoDoAno(driver, posicaoAnoNoLayout)
    time.sleep(5)
    # conexao Banco De Dados
    conexaoDB = DB.create_connection()
    #resultadoVerificacaoExistencia = verificarEclickDeEnviar(driver, conexaoDB, idCidadeAnoStatus)
    time.sleep(5)


    print(parametros)
acessarPaginaPrincipal()


