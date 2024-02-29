'''
    Vai criar a pasta e vai salvar um json com as informações dentro
'''
import os
from Ultils.pastas.nomeDasPastas import gerarJson,removerCaracteresReservados,cortarString



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
    id = ' ' + dados["portaria"]
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






