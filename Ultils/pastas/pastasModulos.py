'''
    Vai criar a pasta e vai salvar um json com as informações dentro
'''
import os
import re
from Ultils.pastas.nomeDasPastas import gerarJson,removerCaracteresReservados,cortarString

#Licitação
#Contrato

def contrato(dadosName,directory):

    # Nome pasta
    nomePadrao = "N°"+dadosName["numero"]
    nomePadrao = cortarString(nomePadrao,10)
    numeroLink = pegarNumeroDoLink(dadosName['link'])
    id = ' '+ numeroLink
    nomeMaisId = nomePadrao + id
    newDir = removerCaracteresReservados(nomeMaisId)

    #Caminho
    file_dir = os.path.join(directory, newDir)
    newFile = criarPasta(file_dir)

    return newFile

def licitacao(dadosName,directory):
    # Nome pasta
    nomePadrao = "N°" + dadosName["numero"]
    nomePadrao = cortarString(nomePadrao, 10)
    numeroLink = pegarNumeroDoLink(dadosName['link'])
    id = ' ' + numeroLink
    nomeMaisId = nomePadrao + id
    newDir = removerCaracteresReservados(nomeMaisId)

    # Caminho
    file_dir = os.path.join(directory, newDir)
    newFile = criarPasta(file_dir)

    return newFile
def criarPasta(file_dir):
    try:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        else:
            print(f"A pasta '{file_dir}' já existe.")
    except Exception as e:
        print(f"\n\n\tErro ao criar a pasta '{file_dir}': {e} \n\n")

    return file_dir

def pegarNumeroDoLink(link):
    numeroLink = re.search(r'(\d+)$', link).group(1)  # Use uma expressão regular para encontrar o número na URL

    return numeroLink





