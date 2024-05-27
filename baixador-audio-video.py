import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Style, Combobox
import threading
import json

class BaixadorYoutube:
    def __init__(self, root):
        self.root = root
        self.root.title("Dowload de Áudio/Vídeo do YouTube")
        self.root.geometry("500x400")

        # Carregar a última pasta de destino salva
        self.arquivo_config = "config.json"
        self.pasta_destino = self.carregar_config()

        self.criar_widgets()

    def criar_widgets(self):
        # Criar campo para o URL do vídeo
        self.rotulo_link = tk.Label(self.root, text="URL do Vídeo do YouTube:")
        self.rotulo_link.pack(pady=5)

        self.entrada_link = tk.Entry(self.root, width=50)
        self.entrada_link.pack(pady=5)
        self.entrada_link.bind("<KeyRelease>", self.resetar_progresso)  # Adiciona o evento de resetar a barra

        # Combobox para selecionar a qualidade do vídeo
        self.rotulo_qualidade = tk.Label(self.root, text="Qualidade do Vídeo:")
        self.rotulo_qualidade.pack(pady=5)
        
        self.opcoes_qualidade = ["best", "worst", "720p", "480p", "360p"]
        self.combobox_qualidade = Combobox(self.root, values=self.opcoes_qualidade)
        self.combobox_qualidade.set("best")
        self.combobox_qualidade.pack(pady=5)

        # Combobox para selecionar o formato do arquivo
        self.rotulo_formato = tk.Label(self.root, text="Formato do Arquivo:")
        self.rotulo_formato.pack(pady=5)
        
        self.opcoes_formato = ["mp4", "webm", "mkv", "wav", "mp3"]
        self.combobox_formato = Combobox(self.root, values=self.opcoes_formato)
        self.combobox_formato.set("mp4")
        self.combobox_formato.pack(pady=5)

        # Botão para escolher a pasta de destino
        self.botao_destino = tk.Button(self.root, text="Escolher Pasta de Destino", command=self.escolher_pasta_destino)
        self.botao_destino.pack(pady=5)

        # Botão para iniciar o download
        self.botao_download = tk.Button(self.root, text="Baixar", command=self.iniciar_download)
        self.botao_download.pack(pady=5)

        # Rótulo e barra de progresso
        self.rotulo_progresso = tk.Label(self.root, text="Progresso:")
        self.rotulo_progresso.pack(pady=5)

        self.estilo = Style(self.root)
        self.estilo.configure("TProgressbar", troughcolor='white', background='blue')

        self.progresso = Progressbar(self.root, orient=tk.HORIZONTAL, length=400, mode='determinate', style="TProgressbar")
        self.progresso.pack(pady=5)

        self.rotulo_estatisticas = tk.Label(self.root, text="")
        self.rotulo_estatisticas.pack(pady=5)

    def escolher_pasta_destino(self):
        # Função para escolher a pasta de destino
        pasta_selecionada = filedialog.askdirectory()
        if pasta_selecionada:
            self.pasta_destino = pasta_selecionada
            self.salvar_config()

    def salvar_config(self):
        # Função para salvar a configuração da pasta de destino
        with open(self.arquivo_config, "w") as arquivo_config:
            json.dump({"pasta_destino": self.pasta_destino}, arquivo_config)

    def carregar_config(self):
        # Função para carregar a configuração da pasta de destino
        if os.path.exists(self.arquivo_config):
            with open(self.arquivo_config, "r") as arquivo_config:
                config = json.load(arquivo_config)
                return config.get("pasta_destino", "")
        return ""

    def iniciar_download(self):
        # Função para iniciar o download
        url_video = self.entrada_link.get()
        if not url_video or not self.pasta_destino:
            messagebox.showerror("Erro", "Por favor, forneça a URL do vídeo e selecione uma pasta de destino.")
            return

        self.thread_download = threading.Thread(target=self.baixar, args=(url_video,))
        self.thread_download.start()

    def baixar(self, url_video):
        qualidade = self.combobox_qualidade.get()
        formato = self.combobox_formato.get()
        if formato in ["wav", "mp3"]:
            self.baixar_audio(url_video, formato)
        else:
            self.baixar_video(url_video, qualidade, formato)

    def baixar_audio(self, url_video, formato):
        # Configurações do yt-dlp para baixar o áudio
        opcoes_ydl = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.pasta_destino, '%(title)s.%(ext)s'),
            'progress_hooks': [self.hook_progresso],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': formato,
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(opcoes_ydl) as ydl:
                ydl.download([url_video])
            messagebox.showinfo("Sucesso", "Download de áudio concluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao baixar o áudio: {e}")

    def baixar_video(self, url_video, qualidade, formato):
        # Configurações do yt-dlp para baixar o vídeo
        if qualidade.isdigit():
            quality_format = f'bestvideo[height<={qualidade}]+bestaudio/best'
        else:
            quality_format = 'bestvideo+bestaudio/best'

        opcoes_ydl = {
            'format': quality_format,
            'outtmpl': os.path.join(self.pasta_destino, '%(title)s.%(ext)s'),
            'merge_output_format': formato,
            'progress_hooks': [self.hook_progresso],
        }

        try:
            with yt_dlp.YoutubeDL(opcoes_ydl) as ydl:
                ydl.download([url_video])
            messagebox.showinfo("Sucesso", "Download de vídeo concluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao baixar o vídeo: {e}")

    def hook_progresso(self, d):
        # Função para atualizar a barra de progresso
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes')
            if total_bytes and downloaded_bytes:
                percentual_progresso = int(downloaded_bytes / total_bytes * 100)
                self.progresso['value'] = percentual_progresso
                self.rotulo_estatisticas.config(text=f"{percentual_progresso}%")
            else:
                self.progresso['value'] = 0
                self.rotulo_estatisticas.config(text="Calculando...")

        elif d['status'] == 'finished':
            self.progresso['value'] = 100
            self.rotulo_estatisticas.config(text="Finalizando")
            self.estilo.configure("TProgressbar", background='green')  # Muda a cor para verde quando concluído

    def resetar_progresso(self, event):
        # Função para resetar a barra de progresso
        self.progresso['value'] = 0
        self.rotulo_estatisticas.config(text="")
        self.estilo.configure("TProgressbar", background='blue')  # Reseta a cor para azul

if __name__ == "__main__":
    root = tk.Tk()
    app = BaixadorYoutube(root)
    root.mainloop()
