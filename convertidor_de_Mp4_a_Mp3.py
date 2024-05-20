import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pytube import YouTube
from moviepy.editor import *
import os
import ssl
import threading

ssl._create_default_https_context = ssl._create_unverified_context

def descargar_youtube():
    """
    Descarga un video de YouTube y lo convierte a formato MP3.

    Parámetros:
    - url: La URL del video de YouTube a descargar.
    - carpeta_destino: La carpeta de destino donde se guardará el archivo MP3.

    Excepciones:
    - Se lanzará una excepción si ocurre algún error durante la descarga o conversión del video.

    Resultado:
    - Muestra un mensaje de éxito si la descarga y conversión se realizan correctamente.
    - Muestra un mensaje de error si ocurre algún problema durante el proceso.
    """
    global yt, video, video_descargado
    url = url_entry.get()
    carpeta_destino = carpeta_entry.get()

    try:
        # Descargar el video de YouTube
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        video_descargado = video.download(output_path=carpeta_destino)

        # Convertir el video a MP3
        video_clip = AudioFileClip(video_descargado)
        nombre_mp3 = carpeta_destino + '/' + yt.title + '.mp3'
        video_clip.write_audiofile(nombre_mp3)

        # Eliminar el archivo de video
        video_clip.close()
        os.remove(video_descargado)

        messagebox.showinfo("Éxito", "El video se descargó y convirtió correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def reiniciar_conversion():
    global yt, video, video_descargado
    try:
        os.remove(video_descargado)
    except:
        pass
    descargar_youtube()

def actualizar_progreso():
    if not video or not video_descargado:
        return

    video_size = video.filesize
    while os.path.exists(video_descargado):
        downloaded_size = os.path.getsize(video_descargado)
        progreso = min(100, int(downloaded_size / video_size * 100))
        progress_bar['value'] = progreso
        progreso_label.config(text=f"{progreso}%")
        ventana.update()
        if progreso == 100:
            break
    progress_bar['value'] = 0
    progreso_label.config(text="")

# Crear ventana
ventana = tk.Tk()
ventana.title("Descargar video de YouTube")

# Etiqueta y entrada para la URL
url_label = tk.Label(ventana, text="URL de YouTube:")
url_label.grid(row=0, column=0, padx=5, pady=5)
url_entry = tk.Entry(ventana, width=50)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

# Etiqueta y entrada para la carpeta destino
carpeta_label = tk.Label(ventana, text="Carpeta destino:")
carpeta_label.grid(row=1, column=0, padx=5, pady=5)
carpeta_entry = tk.Entry(ventana, width=50)
carpeta_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

# Botón para descargar
descargar_btn = tk.Button(ventana, text="Descargar", command=descargar_youtube)
descargar_btn.grid(row=2, column=1, padx=5, pady=5)

# Botón para reiniciar la conversión
reiniciar_btn = tk.Button(ventana, text="Reiniciar", command=reiniciar_conversion)
reiniciar_btn.grid(row=2, column=2, padx=5, pady=5)

# Botón para salir
salir_btn = tk.Button(ventana, text="Salir", command=ventana.quit)
salir_btn.grid(row=2, column=3, padx=5, pady=5)

# Barra de progreso
progress_bar = ttk.Progressbar(ventana, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

# Etiqueta para mostrar el progreso
progreso_label = tk.Label(ventana, text="")
progreso_label.grid(row=3, column=3, padx=5, pady=5)

# Iniciar hilo para actualizar la barra de progreso
threading.Thread(target=actualizar_progreso, daemon=True).start()

# Ejecutar ventana
ventana.mainloop()
