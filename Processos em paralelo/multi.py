import time

import random

array = list(range(1, 20000))
print(array)



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

# Dividir a lista par
parte1_par, parte2_par = dividir_lista(array)
print("Parte 1 (Par):", parte1_par)
print("Parte 2 (Par):", parte2_par)



# Registra o tempo de término
fim = time.perf_counter()

# Calcula o tempo total de execução
tempo_total = fim - inicio

print("tempo de execução",tempo_total)