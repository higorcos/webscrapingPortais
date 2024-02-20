import pandas as pd

def CSV(dados,diretorio):

        # Criar DataFrame a partir do dicionário
        df = pd.DataFrame(dados)

        # Caminho do arquivo CSV
        caminho_arquivo = ""+diretorio+".csv"

        # Salvar os dados em um arquivo CSV usando o Pandas
        df.to_csv(caminho_arquivo, index=False)

        print("Arquivo ",caminho_arquivo," criado");

