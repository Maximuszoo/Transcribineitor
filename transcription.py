from PyQt5.QtCore import QThread, pyqtSignal
import whisper
from pydub import AudioSegment
from utils import write_to_file, remove_temp_files

# Configuración del modelo Whisper
model = whisper.load_model("base")

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
        remove_temp_files(self.segments)
