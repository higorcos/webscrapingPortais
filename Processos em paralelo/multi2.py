import time
import concurrent.futures

array = list(range(1, 20000))



# Registra o tempo de início
inicio = time.perf_counter()
def dividir_lista(lista):
    meio = len(lista) // 2
    if len(lista) % 2 == 0:  # Se o comprimento da lista for par
        parte1 = lista[:meio]
        parte2 = lista[meio:]
    else:  # Se o comprimento da lista for ímpar
        parte1 = lista[:meio + 1]
        parte2 = lista[meio + 1:]
    return parte1, parte2

def calculo_soma(number):
    print("Iniciando a Função...")

    soma=0
    for i in range(number):
        soma = i

    print("Função foi concluída")
    return soma

if __name__ == "__main__":

    with concurrent.futures.ProcessPoolExecutor() as executor:
        cod1 = executor.submit(calculo_soma, 50_000_000)
        cod2 = executor.submit(calculo_soma, 50000000)

        cod1.result()
        cod2.result()

        # Registra o tempo de término e Calcular o tempo total de execução
        fim = time.perf_counter()
        tempo_total = fim - inicio

        print("tempo de execução", tempo_total)
