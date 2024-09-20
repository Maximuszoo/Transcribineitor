import sys
import os
import whisper
from pydub import AudioSegment
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
                             QVBoxLayout, QLabel, QFileDialog, 
                             QProgressBar, QLineEdit, QHBoxLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Configuración del modelo Whisper
model = whisper.load_model("base")

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

# Clase que ejecuta la transcripción en segundo plano
class TranscriptionThread(QThread):
    progress = pyqtSignal(int)
    status_update = pyqtSignal(str)

    def __init__(self, segments):
        super().__init__()
        self.segments = segments

    def run(self):
        total_segments = len(self.segments)
        transcription = ""

        self.status_update.emit("Transcribiendo")

        for i, segment_path in enumerate(self.segments):
            result = model.transcribe(segment_path)
            transcription += result['text'] + " "
            self.progress.emit((i + 1) * 100 // total_segments)

        write_to_file(transcription)
        self.status_update.emit("Finalizado")

        # Eliminar archivos WAV después de la transcripción
        for segment_path in self.segments:
            os.remove(segment_path)

# Función para escribir la transcripción en un archivo
def write_to_file(text):
    with open("Transcripcion.txt", "w") as file:
        file.write(text)

# Clase principal de la interfaz
class Transcribineitor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Transcribineitor 3000")
        self.setGeometry(300, 300, 600, 300)

        # Layout principal vertical
        layout = QVBoxLayout()

        # Grupo de selección de archivo (label + entry + botón)
        file_layout = QHBoxLayout()
        
        # Etiqueta para el cuadro de texto de la ruta del archivo
        self.file_path_label = QLabel("Ruta del archivo:", self)
        file_layout.addWidget(self.file_path_label)

        # Campo de entrada para la ruta del archivo
        self.file_path_entry = QLineEdit(self)
        file_layout.addWidget(self.file_path_entry)

        # Botón para seleccionar archivo
        self.select_button = QPushButton("Seleccionar", self)
        self.select_button.setStyleSheet("background-color: #1C8CDB; color: white;")
        self.select_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.select_button)

        layout.addLayout(file_layout)

        # Botones para acciones principales (transcripción)
        button_layout = QHBoxLayout()

        # Botón para iniciar transcripción
        self.start_button = QPushButton("Iniciar Transcripción", self)
        self.start_button.setStyleSheet("background-color: #1C8CDB; color: white;")
        self.start_button.clicked.connect(self.start_transcription)
        button_layout.addWidget(self.start_button)

        layout.addLayout(button_layout)

        # Barra de progreso
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # Etiqueta de estado
        self.status_label = QLabel("Estado: No Iniciado", self)
        layout.addWidget(self.status_label)

        # Botón para cerrar el programa (separado para evitar acciones accidentales)
        self.close_button = QPushButton("Cerrar", self)
        self.close_button.setStyleSheet("background-color: #1C8CDB; color: white;")
        self.close_button.clicked.connect(self.close_program)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo de audio/video", "", 
            "Audio files (*.wav *.mp3 *.mp4 *.avi *.m4a *.flac);;All files (*.*)"
        )
        if file_path:
            self.file_path_entry.setText(file_path)
            self.progress_bar.setValue(0)

    def start_transcription(self):
        file_path = self.file_path_entry.text()
        if file_path:
            segments = split_audio(file_path)
            self.transcription_thread = TranscriptionThread(segments)
            self.transcription_thread.progress.connect(self.progress_bar.setValue)
            self.transcription_thread.status_update.connect(self.update_status)
            self.transcription_thread.start()

    def update_status(self, text):
        self.status_label.setText(f"Estado: {text}")

    def close_program(self):
        self.close()

# Configuración de la aplicación PyQt5
if __name__ == '__main__':
    app = QApplication(sys.argv)
    transcribineitor = Transcribineitor()
    transcribineitor.show()
    sys.exit(app.exec_())
