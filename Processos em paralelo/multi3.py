import time
import concurrent.futures
# Registra o tempo de início
inicio = time.perf_counter()
import multi2

if __name__ == "__main__":

    with concurrent.futures.ProcessPoolExecutor() as executor:
       numbers = [50_000_000,50_000_000,50]
       cods = executor.map(multi2.calculo_soma, numbers)



    # Registra o tempo de término e Calcular o tempo total de execução
    fim = time.perf_counter()
    tempo_total = fim - inicio

    print("tempo de execução", tempo_total)

