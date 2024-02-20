import requests
import os


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

                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)

                # Salvar o conteúdo do arquivo dentro da pasta individual
                file_path = os.path.join(file_dir, filename)
                with open(file_path, 'wb') as f:
                    f.write(response.content)

                #print(f"Baixado com sucesso \n")
                return {'status Donwload':"Sucesso"}
            else:
                print(f"Erro ao baixar o arquivo do link '{link}': Código de status {response.status_code}")
                return {'status Donwload':"Erro na Resposta do link"}
        except Exception as e:
            print(f"Erro ao baixar o arquivo do link '{link}': {e}")
            return {'status Donwload': "Erro ao Baixar"}
    else:
        print(f"O link '{link}' não é um link para um arquivo conhecido, ignorando...")
        return {'status Donwload': "Link não é um arquivo"}
