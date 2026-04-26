import os

def get_file_info(message):
    if message.document:
        return message.document.file_name, message.document.file_size
    elif message.video:
        return message.video.file_name or "video.mp4", message.video.file_size
    elif message.audio:
        return message.audio.file_name or "audio.mp3", message.audio.file_size
    return "file", 0
  
