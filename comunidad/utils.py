from django.core.files.base import ContentFile
from django.conf import settings
# from moviepy.editor import    
import base64
import os


EXTENSIONES_PERMITIDAS = ['gif', 'png', 'jpeg', 'jpg', 'jfif',
                          'mp4', 'avi', 'wmv', 'flv',
                          'mp3', 'wav', 'opus', 'wma']

tipo_archivo = {
    'ogg': 'opus',
    'x-ms-wma': "wma",
    'mpeg': 'mp3',
    'x-wav': 'wav',
    'x-msvideo': 'avi',
    'x-ms-wmv': 'wmv',
    'x-ms-asf': 'wmv',
    'x-flv': 'flv',
    'mp4': 'mp4'
}

enum_media = {
    'image': 'IMG',
    'audio': 'AUD',
    'video': 'VID'
}

video_codecs = {
    "mp4": "libx264",
    "avi": "mpeg4",
    "wmv": "mpeg4",
    "flv": "libx264"
}


def obtener_extension(formato):
    if formato in tipo_archivo:
        return tipo_archivo[formato]
    return formato


def fileb64decode(archivo, id_user):
    try:
        info, contenido = archivo.split(";base64,")
        mime_type, ext = info.split('/')
        media = mime_type.split(':')[-1]

        ext = obtener_extension(ext)
        if not (ext in EXTENSIONES_PERMITIDAS):
            return {"message": "Formato de archivo no permitido."}

        return [enum_media[media], ContentFile(base64.b64decode(contenido), name=f"{media}_{id_user}." + ext)]
    except:
        return {"message": "Error al subir el archivo."}


def eliminar_archivo(archivo):
    if archivo and os.path.exists(archivo.path):
        if archivo.name != 'avatar.png' and archivo.name != 'portada.jpg':
            os.remove(archivo.path)


def procesar_video(id, path, name):
    # video = VideoFileClip(path)
    # video_resized = video.resize(0.5)
    filebasename = os.path.basename(name)
    old_filename = filebasename.split(".")[0]
    old_extension = filebasename.split(".")[1]
    new_filename = f'{old_filename}_{id}_resized.{old_extension}'
    # ruta = f'{settings.MEDIA_ROOT}/historias/{new_filename}'
    # video_resized.write_videofile(ruta, rewrite_audio=False, preset='faster', codec=video_codecs[old_extension])
    # video_resized.close()
    return new_filename
