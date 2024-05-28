# Baixador-Audio-Video
Este projeto é um aplicativo de desktop em Python usando Tkinter para baixar áudio ou vídeo do YouTube, permitindo ao usuário escolher a qualidade e o formato do arquivo. Utiliza a biblioteca yt-dlp para fazer os downloads e FFmpeg para processar os arquivos. Inclui uma interface gráfica com barra de progresso e configuração de pasta de destino.

## Funcionalidades

- Baixar áudio ou vídeo do YouTube
- Escolher a qualidade do vídeo
- Escolher o formato do arquivo
- Salvar a configuração da pasta de destino
- Barra de progresso para visualização do download

## Requisitos

- Python 3.6 ou superior
- `yt-dlp`
- FFmpeg
- Tkinter (geralmente já incluído com Python em sistemas Linux)

## Instalação

### Passo 1: Clonar o repositório

```bash
git clone https://github.com/richard-lino/Baixador-Audio-Video.git
cd Baixador-Audio-Video
```
### Passo 2: Instalar as dependencias

- Linux:
```bash
pip install yt-dlp
sudo apt-get install ffmpeg
```
- Windows:
```bash
pip install yt-dlp
choco install ffmpeg
```
### Passo 3: Executar o script
```bash
python baixador-audio-video.py
```
## Utilização

<p align="center">
  <img src = "gif/ex1.gif">
  <img src = "gif/ex2.gif">
</p>

- Insira a URL do vídeo do YouTube no campo de entrada.
- Escolha a qualidade do vídeo a partir do menu suspenso.
- Escolha o formato do arquivo a partir do menu suspenso.
- Selecione a pasta de destino clicando no botão "Escolher Pasta de Destino".
- Clique em "Baixar" para iniciar o download.
- Acompanhe o progresso do download na barra de progresso.

## Estrutura do Código
### `__`init`__` e criar_widgets
A função **`__`init`__`** inicializa a aplicação, configurando a janela principal e carregando a última pasta de destino salva. A função **criar_widgets** cria todos os elementos da interface gráfica, incluindo campos de entrada, botões, menus suspensos e a barra de progresso.

### Escolher Pasta de Destino
A função **escolher_pasta_destino** permite ao usuário selecionar a pasta onde os arquivos baixados serão salvos. Essa configuração é salva em um arquivo JSON para ser carregada na próxima execução do programa.

### Iniciar Download
A função **iniciar_download** verifica se a URL do vídeo e a pasta de destino foram fornecidas, e então inicia o download em uma nova thread para evitar que a interface gráfica trave durante o download.

### Baixar Áudio ou Vídeo
Dependendo das escolhas do usuário, a função **baixar** chama **baixar_audio** ou **baixar_video** com as configurações apropriadas. O yt-dlp é configurado para baixar o melhor áudio ou vídeo disponível e converter o arquivo se necessário.

### Atualizar Progresso
A função **hook_progresso** atualiza a barra de progresso e o rótulo de estatísticas com base no status do download. Quando o download é concluído, a cor da barra de progresso é alterada para verde.

### Resetar Progresso
A função **resetar_progresso** reseta a barra de progresso para zero e redefine a cor para azul quando uma nova URL é inserida.

