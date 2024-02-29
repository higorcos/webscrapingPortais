import re
import unicodedata

def removerCaracteresReservados(texto):
    # Remover acentos e caracteres especiais
    texto_sem_acentos = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

    # Remover caracteres reservados
    texto_sem_acentos = texto_sem_acentos.replace('/', '-').replace(':', '-')
    caracteres_reservados = r'[<>:"/\\|?*]'
    texto_sem_caracteres_reservados = re.sub(caracteres_reservados, '', texto_sem_acentos)

    return texto_sem_caracteres_reservados

def cortarString(string, tamanhoMaxString=14):
    # Verifica se a string está vazia ou só contém espaços em branco
    if not string.strip():
        return ''

    # Remove espaços em branco no início e no final da string
    string = string.strip()

    # Encontra o índice do primeiro espaço em branco na string
    index_espaco = string.find(' ')

    # Se não houver espaço em branco ou se a substring até o espaço tiver 14 caracteres ou menos, retorna a substring até o espaço
    if index_espaco == -1 or index_espaco <= tamanhoMaxString:
        return string[:index_espaco]

    # Caso contrário, retorna apenas os primeiros 14 caracteres da substring até o espaço
    return string[:tamanhoMaxString]


def gerarJson(dados,diretory):
    import json

    # Nome do arquivo JSON
    nome_arquivo = diretory+"/dados.json"

    # Escrevendo os dados no arquivo JSON
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False)


