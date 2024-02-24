import pandas as pd
import os

def criarCSV(dados,diretorio):

        # Criar DataFrame a partir do dicionário
        df = pd.DataFrame(dados)

        # Caminho do arquivo CSV
        caminho_arquivo = ""+diretorio+".csv"

        # Salvar os dados em um arquivo CSV usando o Pandas
        df.to_csv(caminho_arquivo, index=False)

        ##print("\t\tArquivo com informações foi criado");
def editarCSV(dados,diretorio):

        if not os.path.exists(diretorio+'.csv'):
                # Se o arquivo não existir, chame a função criarCSV()
                criarCSV(dados,diretorio)
        else:
                # Carregar o arquivo CSV existente como DataFrame
                df_existente = pd.read_csv(diretorio+'.csv')

                # Criar um DataFrame para a nova linha
                df_nova_linha = pd.DataFrame(dados)

                # Anexar a nova linha ao DataFrame existente
                df_atualizado = pd.concat([df_existente, df_nova_linha], ignore_index=True)

                # Salvar o DataFrame atualizado de volta ao arquivo CSV
                df_atualizado.to_csv(diretorio+'.csv', index=False)

                ##print("\t\tInformações adicionadas ao arquivo")

#dados = {'Nome': ['Joana'], 'Idade': [28], 'Profissão': ['Engenheira']}
#diretorio = 'dados'
#editarCSV(dados,diretorio);
