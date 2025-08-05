from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QProgressBar)
from PyQt5.QtCore import Qt
from transcription import TranscriptionThread, split_audio
from style_loader import CSSToQSSConverter
from config_manager import ConfigManager
import os

class Transcribineitor(QWidget):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        
        # Cargar la preferencia del tema guardada
        self.dark_mode = self.config_manager.get_dark_mode()
        
        self.init_ui()
        self.apply_styles()
        
        # Actualizar el texto del botón según el tema cargado
        self.update_theme_button_text()

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
        self.file_path_label = QLabel("Archivo de audio:", self)
        self.file_path_entry = QLineEdit(self)
        self.file_path_entry.setPlaceholderText("Selecciona un archivo de audio...")
        self.select_button = QPushButton("Seleccionar", self)
        self.select_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.file_path_entry)
        file_layout.addWidget(self.select_button)
        layout.addLayout(file_layout)

        # Grupo de destino de transcripción
        output_layout = QHBoxLayout()
        output_layout.setSpacing(10)
        self.output_path_label = QLabel("Guardar como:", self)
        self.output_path_entry = QLineEdit(self)
        self.output_path_entry.setPlaceholderText("Selecciona dónde guardar la transcripción...")
        self.output_select_button = QPushButton("Guardar en...", self)
        self.output_select_button.clicked.connect(self.select_output_file)
        output_layout.addWidget(self.output_path_label)
        output_layout.addWidget(self.output_path_entry)
        output_layout.addWidget(self.output_select_button)
        layout.addLayout(output_layout)

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
        
        # Guardar la preferencia del tema
        self.config_manager.set_dark_mode(self.dark_mode)
        
        # Actualizar el texto del botón
        self.update_theme_button_text()
        
        # Aplicar los nuevos estilos
        self.apply_styles()

    def update_theme_button_text(self):
        """Actualiza el texto del botón de tema según el estado actual"""
        if self.dark_mode:
            self.theme_toggle_button.setText("☀️ Modo Claro")
        else:
            self.theme_toggle_button.setText("🌙 Modo Oscuro")

    def select_file(self):
        # Usar el último directorio usado para archivos de audio
        initial_dir = self.config_manager.get_last_audio_directory()
        if not initial_dir or not os.path.exists(initial_dir):
            initial_dir = os.getcwd()
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar archivo de audio", 
            initial_dir,
            "Archivos de Audio (*.mp3 *.wav *.m4a *.flac *.ogg);;Todos los archivos (*)"
        )
        if file_path:
            self.file_path_entry.setText(file_path)
            
            # Guardar el directorio para la próxima vez
            audio_dir = os.path.dirname(file_path)
            self.config_manager.set_last_audio_directory(audio_dir)
            
            # Sugerir automáticamente un nombre para el archivo de salida
            self.suggest_output_filename(file_path)

    def select_output_file(self):
        """Permite al usuario seleccionar dónde guardar la transcripción"""
        # Obtener el directorio inicial - priorizar último directorio de salida usado
        initial_dir = self.config_manager.get_last_output_directory()
        
        # Si no hay directorio de salida previo, usar el directorio del archivo de audio
        if not initial_dir or not os.path.exists(initial_dir):
            if self.file_path_entry.text():
                initial_dir = os.path.dirname(self.file_path_entry.text())
            else:
                initial_dir = os.getcwd()
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar transcripción como",
            initial_dir,
            "Archivos de texto (*.txt);;Archivos de subtítulos (*.srt);;Todos los archivos (*)"
        )
        if file_path:
            self.output_path_entry.setText(file_path)
            
            # Guardar el directorio de salida para la próxima vez
            output_dir = os.path.dirname(file_path)
            self.config_manager.set_last_output_directory(output_dir)

    def suggest_output_filename(self, audio_path):
        """Sugiere automáticamente un nombre para el archivo de transcripción"""
        if audio_path:
            # Obtener el nombre del archivo sin extensión
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            # Obtener el directorio del archivo de audio
            audio_dir = os.path.dirname(audio_path)
            # Crear el nombre sugerido
            suggested_name = os.path.join(audio_dir, f"{base_name}_transcripcion.txt")
            self.output_path_entry.setText(suggested_name)

    def start_transcription(self):
        file_path = self.file_path_entry.text()
        output_path = self.output_path_entry.text()
        
        if not file_path:
            self.status_label.setText("Estado: Error - No se ha seleccionado ningún archivo de audio")
            return
            
        if not output_path:
            self.status_label.setText("Estado: Error - No se ha especificado dónde guardar la transcripción")
            return
        
        # Verificar que el directorio de salida existe
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            self.status_label.setText("Estado: Error - El directorio de salida no existe")
            return
        
        # Dividir el audio en segmentos
        self.status_label.setText("Estado: Dividiendo audio...")
        segments = split_audio(file_path)
        
        # Iniciar el hilo de transcripción con la ruta de salida personalizada
        self.transcription_thread = TranscriptionThread(segments, output_path)
        self.transcription_thread.progress.connect(self.progress_bar.setValue)
        self.transcription_thread.status_update.connect(self.update_status)
        self.transcription_thread.finished.connect(self.transcription_finished)
        self.transcription_thread.start()
        
        # Deshabilitar botones durante la transcripción
        self.start_button.setEnabled(False)
        self.select_button.setEnabled(False)
        self.output_select_button.setEnabled(False)

    def update_status(self, text):
        self.status_label.setText(f"Estado: {text}")

    def transcription_finished(self):
        output_path = self.output_path_entry.text()
        filename = os.path.basename(output_path) if output_path else "archivo"
        self.status_label.setText(f"Estado: Transcripción completada y guardada como '{filename}'")
        
        # Reactivar botones
        self.start_button.setEnabled(True)
        self.select_button.setEnabled(True)
        self.output_select_button.setEnabled(True)
        self.progress_bar.setValue(100)

    def close_program(self):
        self.close()
