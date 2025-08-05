import os

def write_to_file(text, output_path="Transcripcion.txt"):
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)

def remove_temp_files(segments):
    for segment in segments:
        os.remove(segment)
