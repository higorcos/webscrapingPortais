import time
import os
def download(directory, timeout=350):
    """
    Monitora o diretório de download até que um arquivo apareça ou o tempo limite seja atingido.

    Args:
    - directory (str): O diretório para monitorar.
    - timeout (int): O tempo limite em segundos para a espera do arquivo. Padrão é 60 segundos.

    Returns:
    - str: O caminho do arquivo mais recentemente modificado.
    - None: Se o tempo limite for atingido e nenhum arquivo for encontrado.
    """
    start_time = time.time()
    while True:
        files = os.listdir(directory)
        if files:
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(directory, x)))
            return os.path.join(directory, latest_file)
        if time.time() - start_time > timeout:
            return None
        time.sleep(1)  # Esperar um segundo antes de verificar novamente

