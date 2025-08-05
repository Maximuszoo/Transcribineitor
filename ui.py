from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QFileDialog, QProgressBar)
from PyQt5.QtCore import Qt
from transcription import TranscriptionThread, split_audio
from style_loader import CSSToQSSConverter
import os

class Transcribineitor(QWidget):
    def __init__(self):
        super().__init__()
        self.dark_mode = False  # Estado del tema
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        self.setWindowTitle("Transcribineitor 3000")
        self.setGeometry(300, 300, 700, 400)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header con botón de tema
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        # Título
        title_label = QLabel("Transcribineitor 3000", self)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        header_layout.addWidget(title_label)
        
        # Espaciador
        header_layout.addStretch()
        
        # Botón de cambio de tema
        self.theme_toggle_button = QPushButton("🌙 Modo Oscuro", self)
        self.theme_toggle_button.setObjectName("themeToggle")
        self.theme_toggle_button.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_toggle_button)
        
        layout.addLayout(header_layout)

        # Grupo de selección de archivo
        file_layout = QHBoxLayout()
        file_layout.setSpacing(10)
        self.file_path_label = QLabel("Ruta del archivo:", self)
        self.file_path_entry = QLineEdit(self)
        self.select_button = QPushButton("Seleccionar", self)
        self.select_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.file_path_entry)
        file_layout.addWidget(self.select_button)
        layout.addLayout(file_layout)

        # Botones de acción
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.start_button = QPushButton("Iniciar Transcripción", self)
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
        self.close_button.clicked.connect(self.close_program)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def apply_styles(self):
        """Aplica estilos basados en el archivo CSS"""
        # Obtener la ruta del archivo CSS
        css_file_path = os.path.join(os.path.dirname(__file__), 'styles.css')
        
        # Crear el convertidor y generar QSS
        converter = CSSToQSSConverter()
        qss = converter.generate_qss(css_file_path, self.dark_mode)
        
        # Aplicar los estilos
        self.setStyleSheet(qss)
        
        # Aplicar ID específico para el label de estado
        self.status_label.setObjectName("statusLabel")

    def toggle_theme(self):
        """Cambia entre modo claro y oscuro"""
        self.dark_mode = not self.dark_mode
        
        # Actualizar el texto del botón
        if self.dark_mode:
            self.theme_toggle_button.setText("☀️ Modo Claro")
        else:
            self.theme_toggle_button.setText("🌙 Modo Oscuro")
        
        # Aplicar los nuevos estilos
        self.apply_styles()

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar archivo de audio", 
            "", 
            "Archivos de Audio (*.mp3 *.wav *.m4a *.flac *.ogg);;Todos los archivos (*)"
        )
        if file_path:
            self.file_path_entry.setText(file_path)

    def start_transcription(self):
        file_path = self.file_path_entry.text()
        if not file_path:
            self.status_label.setText("Estado: Error - No se ha seleccionado ningún archivo")
            return
        
        # Dividir el audio en segmentos
        self.status_label.setText("Estado: Dividiendo audio...")
        segments = split_audio(file_path)
        
        # Iniciar el hilo de transcripción
        self.transcription_thread = TranscriptionThread(segments)
        self.transcription_thread.progress.connect(self.progress_bar.setValue)
        self.transcription_thread.status_update.connect(self.update_status)
        self.transcription_thread.finished.connect(self.transcription_finished)
        self.transcription_thread.start()
        
        # Deshabilitar el botón durante la transcripción
        self.start_button.setEnabled(False)

    def update_status(self, text):
        self.status_label.setText(f"Estado: {text}")

    def transcription_finished(self):
        self.status_label.setText("Estado: Transcripción completada y guardada en Transcripcion.txt")
        self.start_button.setEnabled(True)
        self.progress_bar.setValue(100)

    def close_program(self):
        self.close()
