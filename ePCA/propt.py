import json
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By


# Função para salvar cookies em um arquivo
def save_cookies(driver, path):
    with open(path, 'w') as file:
        json.dump(driver.get_cookies(), file)


# Função para carregar cookies de um arquivo
def load_cookies(driver, path):
    with open(path, 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)


# Função para capturar cookies e salvá-los a cada minuto
def capture_cookies():
    driver = webdriver.Chrome()
    driver.set_window_size(800, 1000);
    driver.get('https://app2.tcema.tc.br/PCA/visualizarestrutura.zul')  # URL do site

    # Realize o login ou outras ações necessárias


    # Salve os cookies a cada minuto
    while True:
        time.sleep(30)  # A cada 1 minuto
        sair = driver.find_element(By.XPATH,
                                   '/html/body/div/div[4]/div[1]/div[1]/div/div/div[3]/table/tbody/tr/td/table/tbody/tr/td[17]/button')
        sair.click()
        time.sleep(0.6)
        driver.back()
        time.sleep(0.4)
        save_cookies(driver, 'cookies.json')
        print("Cookies salvos.")

    driver.quit()


# Função para usar cookies salvos e manter a sessão ativa
def use_cookies():
    driver = webdriver.Chrome()


    # Carregar cookies do arquivo
    driver.get('https://app2.tcema.tc.br/PCA/visualizarestrutura.zul')  # URL do site
    while True:
        driver.delete_all_cookies()
        time.sleep(0.1)
        load_cookies(driver, 'cookies.json')
        # Atualizar a página para aplicar os cookies
        driver.refresh()
        print("Cookies carregados e sessão ativa.")
        time.sleep(15)

    # Continue com outras ações automatizadas
    # Exemplo:
    # perform_some_action(driver)
    #driver.quit()


# Main function to run capture and use cookies
def main():
    # Crie dois threads, um para capturar cookies e outro para usar cookies
    capture_thread = threading.Thread(target=capture_cookies)
    use_thread = threading.Thread(target=use_cookies)

    # Inicie os threads
    capture_thread.start()
    time.sleep(60)  # Aguarde um pouco antes de iniciar o uso dos cookies
    use_thread.start()

    # Aguarde os threads terminarem (se necessário)
    capture_thread.join()
    use_thread.join()


if __name__ == "__main__":
    main()
