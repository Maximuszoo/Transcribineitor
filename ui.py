from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QFileDialog, QProgressBar)
from transcription import TranscriptionThread, split_audio

class Transcribineitor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Transcribineitor 3000")
        self.setGeometry(300, 300, 600, 300)

        layout = QVBoxLayout()

        # Grupo de selección de archivo
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel("Ruta del archivo:", self)
        self.file_path_entry = QLineEdit(self)
        self.select_button = QPushButton("Seleccionar", self)
        self.select_button.setStyleSheet("background-color: #1C8CDB; color: white;")
        self.select_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.file_path_entry)
        file_layout.addWidget(self.select_button)
        layout.addLayout(file_layout)

        # Botones de acción
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Iniciar Transcripción", self)
        self.start_button.setStyleSheet("background-color: #1C8CDB; color: white;")
        self.start_button.clicked.connect(self.start_transcription)
        button_layout.addWidget(self.start_button)
        layout.addLayout(button_layout)

        # Barra de progreso y estado
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)
        self.status_label = QLabel("Estado: No Iniciado", self)
        layout.addWidget(self.status_label)

        # Botón de cerrar
        self.close_button = QPushButton("Cerrar", self)
        self.close_button.setStyleSheet("background-color: #1C8CDB; color: white;")
        self.close_button.clicked.connect(self.close_program)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", 
            "Audio files (*.wav *.mp3 *.mp4 *.avi *.m4a *.flac);;All files (*.*)")
        if file_path:
            self.file_path_entry.setText(file_path)
            self.progress_bar.setValue(0)

    def start_transcription(self):
        file_path = self.file_path_entry.text()
        if file_path:
            self.select_button.setDisabled(True)
            self.start_button.setDisabled(True)
            self.select_button.setStyleSheet("background-color: #A9A9A9; color: white;")
            self.start_button.setStyleSheet("background-color: #A9A9A9; color: white;")

            segments = split_audio(file_path)
            self.transcription_thread = TranscriptionThread(segments)
            self.transcription_thread.progress.connect(self.progress_bar.setValue)
            self.transcription_thread.status_update.connect(self.update_status)
            self.transcription_thread.finished.connect(self.transcription_finished)
            self.transcription_thread.start()

    def update_status(self, text):
        self.status_label.setText(f"Estado: {text}")

    def transcription_finished(self):
        self.select_button.setDisabled(False)
        self.start_button.setDisabled(False)
        self.select_button.setStyleSheet("background-color: #1C8CDB; color: white;")
        self.start_button.setStyleSheet("background-color: #1C8CDB; color: white;")
        self.status_label.setText("Estado: Finalizado")

    def close_program(self):
        self.close()
