import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import ffmpeg
import os

def selecionar_arquivo():
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo de vídeo",
        filetypes=[("*.*", "*.*")]
    )
    if arquivo:
        entrada_var.set(arquivo)
        status_var.set("Arquivo selecionado: " + os.path.basename(arquivo))

def separar_faixas_de_audio():
    video_input = entrada_var.get()
    if not video_input:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo de vídeo.")
        return
    
    output_dir = os.path.dirname(video_input)
    try:
        for i in range(1, 4):
            output_audio = f"{output_dir}/faixa_audio_{i}.mp3"
            while os.path.exists(output_audio):
                output_audio = output_audio[:-4]+'_new.mp3'
                print(output_audio)

            (
                ffmpeg
                .input(video_input)
                .output(output_audio, map=f'a:{i-1}', acodec='mp3')
                .run(capture_stdout=True, capture_stderr=True)
            )
            log_message(f"Faixa {i} extraída para {output_audio}")
    except ffmpeg._run.Error as e:
        messagebox.showerror("Erro", f"Erro ao executar o FFmpeg: {e.stderr.decode('utf-8')}")
        log_message("Ocorreu um erro ao processar o vídeo.")

def log_message(message):
    text_area.insert(tk.END, message + "\n")
    text_area.see(tk.END)  # Rolagem automática para a última linha

app = tk.Tk()
app.title("Separador de Faixas de Áudio")
app.geometry("500x300")

entrada_var = tk.StringVar()
status_var = tk.StringVar()

btn_selecionar = tk.Button(app, text="Selecionar Arquivo", command=selecionar_arquivo)
btn_selecionar.pack(pady=10)

entrada_label = tk.Label(app, textvariable=entrada_var, wraplength=480)
entrada_label.pack(pady=5)

btn_extrair = tk.Button(app, text="Separar Faixas de Áudio", command=separar_faixas_de_audio)
btn_extrair.pack(pady=10)

text_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, height=10)
text_area.pack(pady=10, fill=tk.BOTH, expand=True)

app.mainloop()
