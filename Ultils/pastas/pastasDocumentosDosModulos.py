'''
    Vai criar a pasta e vai salvar um json com as informações dentro
'''
import os
from Ultils.pastas.nomeDasPastas import gerarJson,removerCaracteresReservados,cortarString
import re

#Andamento
#Documento
#Fiscal

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
    nomePadrao = dados["designacao"]+"-"+dados["nome"]
    nomePadrao = cortarString(nomePadrao)
    nomeDolink = removerNomeDoLink(dados["link"])
    id = limitar_tamanho_nome_arquivo(nomeDolink)
    id = ' ' + id
    nomeMaisId = nomePadrao + id
    newDir = removerCaracteresReservados(nomeMaisId)

    # Caminho
    file_dir = os.path.join(directory, newDir)
    newFile = criarPastaEjson(dados, file_dir)

    return newFile

def criarPastaEjson(dados,file_dir):

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    gerarJson(dados, file_dir)#gerarJson

    return file_dir

def limitar_tamanho_nome_arquivo(nome, tamanho_max=4):
    # Extrair extensão do arquivo
    nome_base, extensao = os.path.splitext(nome)

    # Limitar o tamanho do nome (sem contar a extensão)
    nome_base = nome_base[:tamanho_max]

    # Remover caracteres especiais e espaços
    nome_base = re.sub(r'[^\w\s]', '', nome_base)

    return nome_base + extensao

def removerNomeDoLink(link):
    partes = link.split('/')
    nome_arquivo_com_extensao = partes[-1]
    print(nome_arquivo_com_extensao)
    return nome_arquivo_com_extensao





