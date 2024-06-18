'''
    Vai criar a pasta e vai salvar um json com as informações dentro
'''
import os
from Ultils.pastas.nomeDasPastas import gerarJson,removerCaracteresReservados,cortarString
import re
import uuid
#Andamento
#Documento
#Fiscal
import random
def documentosDeLicitacao(dados,directory):

    # Nome pasta
    nomePadrao = dados["tipo"]
    nomePadrao = cortarString(nomePadrao)
    numero_aleatorio = random.randint(1, 1000)
    id = " "+dados['data'] +" "+ str(numero_aleatorio)
    nomeMaisId = nomePadrao + id
    newDir = removerCaracteresReservados(nomeMaisId)

    #Caminho
    file_dir = os.path.join(directory, newDir)
    newFile = criarPastaEjson(dados,file_dir)

    return newFile
def andamento(dados,directory):

    # Nome pasta
    nomePadrao = dados["tipo"]+'-'+dados["descricao"]
    nomePadrao = cortarString(nomePadrao)
    id = ' '+dados['data']
    nomeMaisId = nomePadrao + id
    newDir = removerCaracteresReservados(nomeMaisId)

    #Caminho
    file_dir = os.path.join(directory, newDir)
    newFile = criarPastaEjson(dados,file_dir)

    return newFile
def diarioWEBSERVER(dados,directory):


    # Generar un UUID (Identificador Único Universal)
    id = uuid.uuid4()
    # Nome pasta
    nomePadrao = diarioLink(dados['Link'])
    nomeMaisId = str(id)
    newDir =  nomeMaisId

    #Caminho
    file_dir = os.path.join(directory, newDir)
    newFile = criarPastaEjson(dados,file_dir)

    return newFile

def diarioTECUPDATE(dados,directory):


    # Generar un UUID (Identificador Único Universal)
    nomePadrao = 'N°'+dados["edicao"] + '-' + dados["tipo"]+"-"
    nomePadrao = cortarString(nomePadrao,20)
    # Nome pasta
    nomeMaisId = str(dados["id"])
    newDir =  nomePadrao+nomeMaisId

    #Caminho
    file_dir = os.path.join(directory, newDir)
    newFile = criarPastaEjson(dados,file_dir)

    return newFile

def diarioLink(link):
    # Expressão regular para extrair o código específico da URL
    padrao = r"/view_diario/([0-9a-f]+)"
    # Procurar o padrão na URL
    match = re.search(padrao, link)
    # Verificar se há correspondência e obter o código específico
    if match:
        codigo = match.group(1)
        return codigo
    else:
        return '00'
def documentosDoContrato(dados,directory):
    # Nome pasta
    nomePadrao = dados["tipo"] + '-' + dados["descricao"]
    nomePadrao = cortarString(nomePadrao)
    id = ' ' + dados['data']
    nomeMaisId = nomePadrao + id
    newDir = removerCaracteresReservados(nomeMaisId)

    # Caminho
    file_dir = os.path.join(directory, newDir)
    newFile = criarPastaEjson(dados, file_dir)

    return newFile

def documentosDeFiscalizacaoDoContrato(dados,directory):
    # Nome pasta
    nomePadrao = "Fiscal"+"-"+dados["nome"]
    nomePadrao = cortarString(nomePadrao)
    nomeDolink = removerNomeDoLink(dados["link"])
    id = limitar_tamanho_nome_arquivo(nomeDolink)
    id = '-' + id
    nomeMaisId = nomePadrao + id
    newDir = removerCaracteresReservados(nomeMaisId)

    # Caminho
    file_dir = os.path.join(directory, newDir)
    newFile = criarPastaEjson(dados, file_dir)

    return newFile

def criarPastaEjson(dados,file_dir):

    try:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        else:
            print(f"")
    except Exception as e:
        print(f"\n\n\tErro ao criar a pasta '{file_dir}': {e} \n\n")

    gerarJson(dados, file_dir)#gerarJson

    return file_dir

def limitar_tamanho_nome_arquivo(nome, tamanho_max=4):
    # Extrair extensão do arquivo
    nome_base, extensao = os.path.splitext(nome)

    # Limitar o tamanho do nome (sem contar a extensão)
    nome_base = nome_base[:tamanho_max]

    # Remover caracteres especiais e espaços
    nome_base = re.sub(r'[^\w\s]', '', nome_base)

    return nome_base

def removerNomeDoLink(link):
    partes = link.split('/')
    nome_arquivo_com_extensao = partes[-1]
    print(nome_arquivo_com_extensao)
    return nome_arquivo_com_extensao





