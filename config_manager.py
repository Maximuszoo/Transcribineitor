import json
import os

class ConfigManager:
    def __init__(self):
        self.config_file = "config.json"
        self.default_config = {
            "dark_mode": False,
            "last_audio_directory": "",
            "last_output_directory": ""
        }
    
    def load_config(self):
        """Carga la configuración desde el archivo, o crea una por defecto"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Agregar claves que falten (para compatibilidad futura)
                for key, value in self.default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            else:
                return self.default_config.copy()
        except (json.JSONDecodeError, FileNotFoundError):
            # Si hay error al leer, usar configuración por defecto
            return self.default_config.copy()
    
    def save_config(self, config):
        """Guarda la configuración en el archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def get_dark_mode(self):
        """Obtiene la preferencia del tema oscuro"""
        config = self.load_config()
        return config.get("dark_mode", False)
    
    def set_dark_mode(self, dark_mode):
        """Guarda la preferencia del tema oscuro"""
        config = self.load_config()
        config["dark_mode"] = dark_mode
        self.save_config(config)
    
    def get_last_audio_directory(self):
        """Obtiene el último directorio usado para archivos de audio"""
        config = self.load_config()
        return config.get("last_audio_directory", "")
    
    def set_last_audio_directory(self, directory):
        """Guarda el último directorio usado para archivos de audio"""
        config = self.load_config()
        config["last_audio_directory"] = directory
        self.save_config(config)
    
    def get_last_output_directory(self):
        """Obtiene el último directorio usado para guardar transcripciones"""
        config = self.load_config()
        return config.get("last_output_directory", "")
    
    def set_last_output_directory(self, directory):
        """Guarda el último directorio usado para guardar transcripciones"""
        config = self.load_config()
        config["last_output_directory"] = directory
        self.save_config(config)
