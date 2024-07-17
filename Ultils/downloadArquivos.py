import requests
import os
import re
from bs4 import BeautifulSoup

def link(link,file_dir):

    # Verificar se o link termina com uma extensão de arquivo comum (por exemplo, .pdf, .doc, .xlsx, etc.)
    if link.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.txt', '.zip')):
        # Baixar o arquivo
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
            # Enviar uma solicitação GET para o URL do link
            response = requests.get(link,headers=headers)

            # Verificar se a solicitação foi bem-sucedida (código de status 200)
            if response.status_code == 200:
                # Extrair o nome do arquivo do URL do link
                filename = os.path.basename(link)
                filename = limitar_tamanho_nome_arquivo(filename)

                # Salvar o conteúdo do arquivo dentro da pasta individual
                file_path = os.path.join(file_dir, filename)
                with open(file_path, 'wb') as f:
                    f.write(response.content)

                #print(f"\n\n\t\tBaixado com sucesso \n")
                return {'status Donwload':"Sucesso", 'link_fuc':link}
            else:
                print(f"\n\n\t\tErro na Resposta do link '{link}': Código de status {response.status_code}")
                return {'status Donwload':"Erro na Resposta do link", 'link_fuc':link}
        except Exception as e:
            print(f"\n\n\t\tErro ao baixar o arquivo do link '{link}': {e}")
            return {'status Donwload': "Erro ao Baixar",'link_fuc':link}
    else:
        print(f"\n\n\t\tO link '{link}' não é um link para um arquivo conhecido, ignorando...")
        return {'status Donwload': "Link não é um arquivo" , 'link_fuc':link}
def limitar_tamanho_nome_arquivo(nome, tamanho_max=3):
    # Extrair extensão do arquivo
    nome_base, extensao = os.path.splitext(nome)

    # Limitar o tamanho do nome (sem contar a extensão)
    nome_base = nome_base[:tamanho_max]

    # Remover caracteres especiais e espaços
    nome_base = re.sub(r'[^\w\s]', '', nome_base)

    return nome_base + extensao
def linkSemExtensao(url, file_dir):
    if url.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.txt')):
        return link(url, file_dir)
    else:
        try:
            # Enviar uma solicitação GET para o URL do link
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
            response = requests.get(url, headers=headers)

            # Verificar se a solicitação foi bem-sucedida (código de status 200)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Encontrar o iframe
                iframe = soup.find('iframe')
                if iframe:
                    iframe_url = iframe['src']
                    # Baixar o arquivo real
                    print('\t\t ------ AQUI ')
                    result = link(iframe_url, file_dir)
                    return result
                else:
                    print("Iframe não encontrado na página.")
                    return {'status Donwload': "Iframe não encontrado"}
            else:
                print(f"\n\n\t\tErro na Resposta do link '{url}': Código de status {response.status_code}")
                return {'status Donwload': "Erro na Resposta do link"}
        except Exception as e:
            print(f"\n\n\t\tErro ao baixar o arquivo do link '{url}': {e}")
            return {'status Donwload': "Erro ao Baixar"}
