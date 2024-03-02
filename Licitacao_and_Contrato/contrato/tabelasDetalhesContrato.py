import os
from Ultils import gerarArquivo, downloadArquivos
from Ultils.pastas import pastasDocumentosDosModulos as criarPastaJson
import concurrent.futures

directoryGlobal = ''
globalParentDirectory = ''


def verificarSeExisteTabelas(soup,directory=''):
    tablesObj = {}

    #Encontrar Tabelas
        #-Fiscalização do contrato
        #-Documentos
    tables = soup.select('.col-xs-12')
    tablesLength = tables.__len__()

    #Não tem tabela
    if tablesLength == 0:
        return []
    #colocar em um objeto as tabelas encontradas
    for i in range(0,tablesLength):

        #Chave = Nome da tabela
        titleTable = tables[i].find_all("div", {"class": "panel-heading"})
        titleTable = titleTable[0].text

        #valores = dados da tabela
        bodyTable = tables[i]

        tablesObj[titleTable] = bodyTable

    #TIPO POSSIVEIS DE TABELAS EM DETALHES DE LICITAÇÃO
    if 'Fiscalização do contrato' in tablesObj:
        #print('\tPossui Tabela de Fiscalização do contrato')
        ficalizacaoDoContrato(tablesObj['Fiscalização do contrato'],directory)


    if 'Documentos' in tablesObj:
        documentos(tablesObj['Documentos'],directory)
        #print('\tPossui tabela de Documentos')

def documentos(table,directory):

    # Criar uma pasta para os downloads (se ela ainda não existir)
    parentDirectory = directory
    directory = directory+"/documentos"
    global directoryGlobal
    directoryGlobal = directory

    if not os.path.exists(directory):
        os.makedirs(directory)

    lines = table.find_all("tr")
    linesTitle = lines[0].find_all("th")
    #Remover titulos das colunas
    lines.pop(0)
    if not lines:
        return []
    print("\tDownload documentos dos contrato")

    title0 = linesTitle[0].text
    title1 = linesTitle[1].text
    title2 = linesTitle[2].text
    title3 = linesTitle[3].text

    dadosTabela = {title0: [], title1: [], title2: [], title3: [], "status": []}


    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.map(pecorrerLinhasDocumentos, lines)

        for dados in result:
            dadosTabela[title0].append(dados[0])
            dadosTabela[title1].append(dados[1])
            dadosTabela[title2].append(dados[2])
            dadosTabela[title3].append(dados[3])
            dadosTabela["status"].append(dados[4])

    print("\t\tBaixou Documentos de Contrato")
    gerarArquivo.criarCSV(dadosTabela, parentDirectory+"/Detalhes Documentos");

def pecorrerLinhasDocumentos(lines):
    colums = lines.find_all()
    colum0 = colums[0].text
    colum1 = colums[1].text
    colum2 = colums[2].text  # data
    colum3 = colums[3].find('a').get('href')  # link
    link = colum3
    #print("\t"+colum0, colum1, colum2, colum3)

    print("\tLINK:" + link);

    dados = {"tipo": colum0, "descricao": colum1, "data": colum2, "link": link}
    # Criar uma pasta e arquivo json com dados
    file_dir = criarPastaJson.documentosDoContrato(dados, directoryGlobal)

    # Verificar se tem link
    if link:
        statusDonwload = downloadArquivos.link(link, file_dir)
    else:
        print("\tLink não encontrado")
        statusDonwload = {'status Donwload': "Link não foi passado"}

    return [colum0,colum1,colum2,link,statusDonwload['status Donwload']]

def ficalizacaoDoContrato(table, directory):
    # Criar uma pasta para os downloads (se ela ainda não existir)
    parentDirectory = directory
    directory = directory + "/ficalizacao"
    global directoryGlobal
    directoryGlobal = directory

    if not os.path.exists(directory):
        os.makedirs(directory)

    lines = table.find_all("tr")
    linesTitle = lines[0].find_all("th")
    # Remover titulos das colunas
    lines.pop(0)
    if not lines:
        #print('nada')
        return []
    print("\tDownload ficalizacao do contrato")
    print(lines.__len__())

    title0 = linesTitle[0].text
    title1 = linesTitle[1].text
    title2 = linesTitle[2].text
    title3 = linesTitle[3].text
    title4 = linesTitle[4].text

    dadosTabela = {title0: [], title1: [], title2: [], title3: [], "link": [], "status": []}


    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.map(pecorrerLinhasFicalizacaoDoContrato, lines)

        for dados in result:
            dadosTabela[title0].append(dados[0])
            dadosTabela[title1].append(dados[1])
            dadosTabela[title2].append(dados[2])
            dadosTabela[title3].append(dados[3])
            dadosTabela['link'].append(dados[4])
            dadosTabela["status"].append(dados[5])

    print("\t\tBaixou Fiscalização de Contrato")
    gerarArquivo.criarCSV(dadosTabela, parentDirectory + "/Detalhes ficalizacao");

def pecorrerLinhasFicalizacaoDoContrato(lines):
    print("\t\tRodando Ficalização")
    colums = lines.find_all()
    colum0 = colums[0].text
    colum1 = colums[1].text
    colum2 = colums[2].text
    colum3 = colums[3].text
    colum4 = colums[4].find('a').get('href')  # link
    link = colum4
    #print("\t"+colum0, colum1, colum2)

    print("\tLINK:" + link);

    dados = {"designacao": colum0, "cpf": colum1, "nome": colum2, "portaria": colum3,"link":link}
    # Criar uma pasta e arquivo json com dados
    file_dir = criarPastaJson.documentosDeFiscalizacaoDoContrato(dados, directoryGlobal)

    # Verificar se tem link
    if link:
        statusDonwload = downloadArquivos.link(link, file_dir)
    else:
        print("\tLink não encontrado")
        statusDonwload = {'status Donwload': "Link não foi passado"}

    return [colum0, colum1, colum2,colum3, link, statusDonwload['status Donwload']]