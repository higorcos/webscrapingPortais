import time
import concurrent.futures
# Registra o tempo de início
inicio = time.perf_counter()

def pecorrerArray(array):
    print("Iniciando a Função...")
    for i in array:
        print(i)
    print(f"Função foi concluída")

if __name__ == "__main__":

    with concurrent.futures.ProcessPoolExecutor() as executor:
       numbers = ["Lista0","Lista1","Lista2"]
       cods = executor.submit(pecorrerArray, numbers)



    # Registra o tempo de término e Calcular o tempo total de execução
    fim = time.perf_counter()
    tempo_total = fim - inicio

    print("tempo de execução", tempo_total)

