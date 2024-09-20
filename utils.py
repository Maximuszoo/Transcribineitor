import os

def write_to_file(text):
    with open("Transcripcion.txt", "w") as file:
        file.write(text)

def remove_temp_files(segments):
    for segment in segments:
        os.remove(segment)
