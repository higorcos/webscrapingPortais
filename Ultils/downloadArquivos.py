import requests
import os
import re

def link(link,file_dir):
    # Verificar se o link termina com uma extensão de arquivo comum (por exemplo, .pdf, .doc, .xlsx, etc.)
    if link.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.txt')):
        # Baixar o arquivo
        try:
            # Enviar uma solicitação GET para o URL do link
            response = requests.get(link)

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
                return {'status Donwload':"Sucesso"}
            else:
                print(f"\n\n\t\tErro na Resposta do link '{link}': Código de status {response.status_code}")
                return {'status Donwload':"Erro na Resposta do link"}
        except Exception as e:
            print(f"\n\n\t\tErro ao baixar o arquivo do link '{link}': {e}")
            return {'status Donwload': "Erro ao Baixar"}
    else:
        print(f"\n\n\t\tO link '{link}' não é um link para um arquivo conhecido, ignorando...")
        return {'status Donwload': "Link não é um arquivo"}
def limitar_tamanho_nome_arquivo(nome, tamanho_max=3):
    # Extrair extensão do arquivo
    nome_base, extensao = os.path.splitext(nome)

    # Limitar o tamanho do nome (sem contar a extensão)
    nome_base = nome_base[:tamanho_max]

    # Remover caracteres especiais e espaços
    nome_base = re.sub(r'[^\w\s]', '', nome_base)

    return nome_base + extensao
def linkSemExtensao(link, file_dir):
    if link.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.txt')):
        return link(link,file_dir);
    else:
        try:
            # Enviar uma solicitação GET para o URL do link
            response = requests.get(link)

            # Verificar se a solicitação foi bem-sucedida (código de status 200)
            if response.status_code == 200:
                # Extrair o nome do arquivo do URL do link
                filename = os.path.basename(link+'.pdf')

                # Salvar o conteúdo do arquivo dentro da pasta especificada
                file_path = os.path.join(file_dir, filename)
                with open(file_path, 'wb') as f:
                    f.write(response.content)

                return {'status Donwload': "Sucesso"}
            else:
                print(f"\n\n\t\tErro na Resposta do link '{link}': Código de status {response.status_code}")
                return {'status Donwload': "Erro na Resposta do link"}
        except Exception as e:
            print(f"\n\n\t\tErro ao baixar o arquivo do link '{link}': {e}")
            return {'status Donwload': "Erro ao Baixar"}
