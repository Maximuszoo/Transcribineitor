# Transcribineitor 3000 🎙️

**Transcribineitor 3000** es una potente herramienta de escritorio diseñada para transcribir archivos de audio a texto de manera automática, precisa y eficiente utilizando la tecnología de inteligencia artificial **OpenAI Whisper**.

Esta aplicación ofrece una interfaz gráfica moderna y fácil de usar, permitiendo a los usuarios convertir sus grabaciones, podcasts o entrevistas en texto plano, con la flexibilidad de elegir dónde guardar los resultados y personalizar su experiencia visual.

---

## 📸 Capturas de Pantalla

<img width="697" height="490" alt="Modo_obscuro" src="https://github.com/user-attachments/assets/4629fdf9-8e54-4049-bc3f-d569b039986c" />
*Modo oscuro*



<img width="699" height="486" alt="Modo_claro" src="https://github.com/user-attachments/assets/2af010b0-79c9-48d5-8050-72912756cef4" />
*Modo claro*

---

## ✨ Características Principales

- **🚀 Transcripción Potente**: Utiliza el modelo `base` de Whisper para un equilibrio óptimo entre velocidad y precisión.
- **🎨 Interfaz Moderna y Personalizable**: GUI construida con PyQt5 con soporte nativo para **Modo Claro y Oscuro**.
- **💾 Gestión de Archivos Flexible**:
    - Selección de archivo de audio de origen.
    - **Selección personalizada de ruta de salida**: Tú decides dónde y con qué nombre guardar la transcripción.
- **🧠 Configuración Inteligente**: Recuerda tus preferencias (tema, últimas carpetas usadas) entre sesiones gracias a su gestor de configuración.
- **📂 Soporte Multi-formato**: Compatible con `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`.
- **⚡ Procesamiento Optimizado**: Divide automáticamente archivos largos en segmentos de 30 segundos para mayor estabilidad.
- **📊 Feedback Visual**: Barra de progreso y actualizaciones de estado en tiempo real.
- **🔒 Privacidad Total**: Todo el procesamiento se realiza localmente en tu máquina.

---

## 🛠️ Requisitos del Sistema

- **Python 3.8** o superior.
- **FFmpeg**: Esencial para el procesamiento de audio.
    - *Linux*: `sudo apt install ffmpeg`
    - *Windows*: Descargar de [ffmpeg.org](https://ffmpeg.org/) y agregar al PATH.
    - *macOS*: `brew install ffmpeg`

---

## 📥 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Maximuszoo/Transcribineitor.git
   cd Transcribineitor
   ```

2. **Crear entorno virtual (Recomendado)**
   ```bash
   python -m venv venv
   # Activar:
   # Windows: venv\Scripts\activate
   # Linux/macOS: source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Uso

1. **Iniciar la aplicación**
   ```bash
   python main.py
   ```

2. **Transcribir un audio**
   1. Haz clic en **"Seleccionar"** y elige tu archivo de audio.
   2. (Opcional) Haz clic en **"Guardar en..."** para elegir dónde guardar el archivo de texto. Si no lo haces, el sistema sugerirá una ubicación automáticamente.
   3. Presiona **"Iniciar Transcripción"**.
   4. Espera a que la barra de progreso se complete.

---

## 📂 Estructura del Proyecto

```
Transcribineitor 3000/
├── main.py              # Punto de entrada
├── ui.py                # Interfaz gráfica (PyQt5)
├── transcription.py     # Lógica de transcripción (Whisper + Threads)
├── config_manager.py    # Gestión de configuración y persistencia
├── style_loader.py      # Sistema de estilos (CSS a QSS)
├── utils.py             # Utilidades de archivos
├── styles.css           # Hoja de estilos
└── config.json          # Archivo de configuración (auto-generado)
```

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas!
1. Fork del proyecto.
2. Crea tu rama (`git checkout -b feature/AmazingFeature`).
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`).
4. Push a la rama (`git push origin feature/AmazingFeature`).
5. Abre un Pull Request.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
