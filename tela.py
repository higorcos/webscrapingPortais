import tkinter as tk
from tkinter import ttk
import time
import sys

# Variáveis de configuração
nomeJanela = "Baixando Arquivos"
nomeTipoDosArquivos = "Licitações"
subtitulo = "Baixando arquivos do portal"
linkDoPortal = "https://transparencia.parnarama.ma.gov.br/acessoInformacao/licitacao/tce"

# Variável global para o total de processos
total_processes = 100

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Rola automaticamente para o final

    def flush(self):
        pass  # Necessário para compatibilidade com sys.stdout

# Função para simular o carregamento
def start_loading():
    global total_processes  # Acessa a variável global total_processes
    for i in range(1, total_processes + 1):
        # Atualiza o valor da barra de progresso
        progress_var.set(i)
        # Atualiza o texto que mostra o progresso atual
        progress_label.config(text=f'{nomeTipoDosArquivos} - Processo {i} de {total_processes}')
        # Atualiza a interface para refletir as mudanças
        window.update_idletasks()
        # Exemplo de saída de comando
        print(f'AQUI - {nomeTipoDosArquivos} - Processo {i}')
        # Pausa para simular o tempo de processamento
        time.sleep(0.05)

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
progress_bar = ttk.Progressbar(window, orient='horizontal', length=300, mode='determinate', variable=progress_var, maximum=total_processes)
progress_bar.pack(pady=20, padx=30)

# Criação do rótulo que mostra o progresso atual
progress_label = tk.Label(window, text=f'{nomeTipoDosArquivos} - Processo 0 de {total_processes}')
progress_label.pack(pady=10)

# Criação do widget de texto para exibir a saída dos comandos
terminal_output = tk.Text(window, height=10, width=50, wrap=tk.NONE)
terminal_output.pack(pady=10, padx=30)

# Redirecionamento da saída padrão para o widget de texto
sys.stdout = StdoutRedirector(terminal_output)

# Inicia o carregamento automaticamente
window.after(100, start_loading)

# Inicia o loop principal da interface gráfica
window.mainloop()
