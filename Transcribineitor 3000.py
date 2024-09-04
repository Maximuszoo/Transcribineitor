import tkinter as tk
from tkinter import filedialog, ttk, StringVar
import whisper
from pydub import AudioSegment
import threading
import os

# Configuración del modelo Whisper
model = whisper.load_model("base")

# Función para convertir el archivo de audio a formato WAV (si no lo está ya)
def convert_to_wav(file_path):
    audio = AudioSegment.from_file(file_path)
    wav_path = file_path.rsplit('.', 1)[0] + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

# Función para dividir el archivo de audio en segmentos de 30 segundos
def split_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    duration = len(audio) // 1000  # Duración en segundos
    segments = []

    for start in range(0, duration, 30):  # 30 segundos por segmento
        end = min(start + 30, duration)
        segment = audio[start*1000:end*1000]  # Convertir a milisegundos
        segment_path = f"{file_path.rsplit('.', 1)[0]}_segment_{start}-{end}.wav"
        segment.export(segment_path, format="wav")
        segments.append(segment_path)

    return segments

# Función para transcribir los segmentos de audio
def transcribe_segments(segments, progress_var, status_label):
    total_segments = len(segments)
    transcription = ""

    status_label_var.set("Transcribiendo")

    for i, segment_path in enumerate(segments):
        print(f"Transcribing segment {i+1}/{total_segments}...")
        result = model.transcribe(segment_path)
        transcription += result['text'] + " "
        progress_var.set((i + 1) / total_segments * 100)

    write_to_file(transcription)
    status_label_var.set("Finalizado")

    # Eliminar archivos WAV después de la transcripción
    for segment_path in segments:
        os.remove(segment_path)

# Función para escribir la transcripción en un archivo
def write_to_file(text):
    with open("Transcripcion.txt", "w") as file:
        file.write(text)

# Función para abrir el cuadro de diálogo de selección de archivo
def select_file():
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo de audio/video",
        filetypes=(("Audio files", "*.wav *.mp3 *.mp4 *.avi *.m4a *.flac"), ("All files", "*.*"))
    )
    if file_path:
        file_path_var.set(file_path)
        progress_var.set(0)  # Reset progress bar

# Función para iniciar la transcripción
def start_transcription():
    file_path = file_path_var.get()
    if file_path:
        status_label_var.set("No Iniciado")
        segments = split_audio(file_path)
        transcribe_thread = threading.Thread(target=transcribe_segments, args=(segments, progress_var, status_label))
        transcribe_thread.start()

# Función para cerrar el programa
def close_program():
    root.quit()

# Configuración de la interfaz gráfica con tkinter
root = tk.Tk()
root.title("Transcribineitor 3000")
root.geometry("500x300")
root.configure(bg="#191414")  # Fondo verde estilo Spotify

# Variables
progress_var = tk.DoubleVar()
file_path_var = StringVar()
status_label_var = StringVar(value="No Iniciado")

# Barra de progreso
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=20, padx=20, fill=tk.X)

# Entry para la ruta del archivo
file_path_entry = tk.Entry(root, textvariable=file_path_var, width=50)
file_path_entry.pack(pady=10)

# Botones
select_button = tk.Button(root, text="Seleccionar Archivo de Audio/Video", command=select_file, bg="#1DB954", fg="#191414")
select_button.pack(pady=10)

start_button = tk.Button(root, text="Iniciar Transcripción", command=start_transcription, bg="#1DB954", fg="#191414")
start_button.pack(pady=10)

close_button = tk.Button(root, text="Cerrar", command=close_program, bg="#1DB954", fg="#191414")
close_button.pack(pady=10)

# Estado de la transcripción
status_label = tk.Label(root, textvariable=status_label_var, bg="#191414", fg="#1DB954")
status_label.pack(pady=10)

# Estilo para widgets
style = ttk.Style()
style.theme_use('clam')
style.configure("TProgressbar", troughcolor="#191414", background="#1DB954")

root.mainloop()
