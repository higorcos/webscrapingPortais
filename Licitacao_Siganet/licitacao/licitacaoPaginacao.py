from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from Licitacao_Siganet.licitacao import detalhesLicitacao
import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
# Variáveis de configuração
nomeJanela = "Baixando Arquivos"
nomeTipoDosArquivos = "Licitações"
subtitulo = "Baixando arquivos do portal"
linkDoPortal = "https://transparencia.parnarama.ma.gov.br/acessoInformacao/licitacao/tce"

# Variável global para o total de processos
total_processes = 436


def janela(driver,directoryInformation,link):
    class StdoutRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget

        def write(self, message):
            self.text_widget.insert(tk.END, message)
            self.text_widget.see(tk.END)  # Rola automaticamente para o final

        def flush(self):
            pass  # Necessário para compatibilidade com sys.stdout

    def start_traversev_thread():
        thread = threading.Thread(target=traversev, args=(driver,directoryInformation,link))
        thread.start()

    def toggle_terminal():
        if terminal_frame.winfo_ismapped():
            terminal_frame.pack_forget()
        else:
            terminal_frame.pack(pady=10, padx=30)
    def traversev(driver, directoryInformation, link):

        # acessar link
        driver.get(link)

        # Aguardar o carregamento da página
        time.sleep(8)

        # Obter o código HTML da página
        html = driver.page_source

        # Analisar o HTML usando BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # numero de paginas
        selectNumberPages = soup.select('#dtLicitacoes_ellipsis+ .paginate_button a')
        numberPages = int(selectNumberPages[0].text)

        linksPagesDetails = []

        # Percorrer páginas
        for i in range(0, numberPages):
            # Aguardar 1 segundo
            # time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # Pegar os links da paginação (array com varios links)
            currentPageLinks = soup.select('#dtLicitacoes a')

            # adicionar cada link no array (adicionar apenas o link)
            for link in currentPageLinks:
                linksPagesDetails.append(link.get('href'))

            if numberPages != i:
                button = driver.find_element(By.CSS_SELECTOR, "#dtLicitacoes_next a");
                button.click();

        #print(linksPagesDetails.__len__())
        num = 0

        total_processes = 2


        for linkPage in linksPagesDetails:
            num += 1
            #print(num)
            # print("Licitação Acessada",linkPage)
            # Atualiza o valor da barra de progresso
            progress_var.set(num)
            # Atualiza o texto que mostra o progresso atual
            progress_label.config(text=f'{nomeTipoDosArquivos} - Processo {num} de {linksPagesDetails.__len__()}')
            # Atualiza a interface para refletir as mudanças
            window.update_idletasks()
            time.sleep(1)


            # abrir uma nova aba
            driver.execute_script("window.open('about:blank', '_blank');")

            # Captura as alças das guias
            janelas = driver.window_handles

            # Troca o foco para a nova aba (a última na lista de alças)
            driver.switch_to.window(janelas[-1])

            # Função que irá cuidar do detalhes da licitação (passando a URL)
            detalhesLicitacao.mostrarDetalhe(driver, directoryInformation, linkPage)

            # Feche a aba atual
            driver.close()
            # Troca o foco para a nova aba (a última na lista de alças)
            driver.switch_to.window(janelas[0])

        return []

    # Criação da janela principal

    window = tk.Tk()
    window.title(nomeJanela)

    # Variável que controla a barra de progresso
    progress_var = tk.IntVar()

    # Criação do subtítulo
    subtitle_label = tk.Label(window, text=subtitulo)
    subtitle_label.pack(pady=10, padx=30)

    # Criação do link do portal
    link_label = tk.Label(window, text=linkDoPortal, fg="blue", cursor="hand2")
    link_label.pack(pady=10, padx=30)

    # ATEnÇãO
    link_label_att = tk.Label(window, text="Não click em nenhum Lugar desse aplicativo", fg="red")
    link_label_att.pack(pady=0, padx=0)
    # ATEnÇãO
    link_label_att = tk.Label(window, text="Entre na pasta de arquivos depois que finalizar tudo", fg="red")
    link_label_att.pack(pady=0, padx=0)

    # Criação da barra de progresso com padding
    progress_bar = ttk.Progressbar(window, orient='horizontal', length=300, mode='determinate', variable=progress_var,
                                   maximum=total_processes)
    progress_bar.pack(pady=20, padx=30)

    # Criação do rótulo que mostra o progresso atual
    progress_label = tk.Label(window, text=f'{nomeTipoDosArquivos} - Processo 0 de {total_processes}')
    progress_label.pack(pady=10)

    # Frame para conter o terminal
    terminal_frame = tk.Frame(window)

    # Criação do widget de texto para exibir a saída dos comandos com fonte reduzida
    terminal_output = tk.Text(terminal_frame, height=10, width=50, wrap=tk.NONE)
    terminal_output.pack(pady=10, padx=30)


    # Botão para alternar a visibilidade do terminal
    toggle_button = tk.Button(window, text="logs", command=toggle_terminal)
    toggle_button.pack(pady=10, padx=30)

    # Redirecionamento da saída padrão para o widget de texto
    sys.stdout = StdoutRedirector(terminal_output)


    # Inicia o carregamento automaticamente
    window.after(100, start_traversev_thread)
    #window.after(100, lambda: traversev(driver,directoryInformation,link))


    # Inicia o loop principal da interface gráfica
    window.mainloop()
def run_traversev():
    '''
    linkLicitacao = "https://transparencia.balsas.ma.gov.br/acessoInformacao/licitacao/tce/exibir";
    nomePortal = "TESTE";
    tipoPortal = "TESTE";


    directoryInformation = {
       "mainFolder": "Downloads-" + nomePortal + "-" + tipoPortal + "",
       "licitacaoFolder": "BBBBB",
    }
    # Criar uma nova instância do driver do Chrome
    driver = webdriver.Chrome()

    # Definir o tamanho da janela
    driver.set_window_size(800, 600);

    traversev(driver, directoryInformation, linkLicitacao)

    # fechar navegador
    driver.quit()
    '''

