import json
import math
import os
import re
import requests
from colorpick import pick
from colorama import Fore, Style
import yt_dlp as ytdlp
from youtubesearchpython import VideosSearch, Video
import climage
from moviepy.editor import *

def print_centered(text):
    width = os.get_terminal_size().columns
    lines = text.splitlines()
    for line in lines:
        clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
        padding = max((width - len(clean_line)) // 2, 0)
        centered_line = ' ' * padding + line
        print(centered_line)

def loadVideo(url, inp, video):
    options = ["🎥 Descargar video", "🎵 Descargar audio", "Volver"]
    option, index = pick(options, "Selecciona el formato de descarga", indicator='>', default_index=1)

    def downloadingScreen():
        image_url = video["thumbnails"][0]['url']
        img_data = requests.get(image_url).content
        with open(video["id"] + '.jpg', 'wb') as handler:
            handler.write(img_data)

        os.system('clear')
        print("")
        print("")
        print("")
        width = os.get_terminal_size().columns
        ascii = climage.convert(video["id"] + '.jpg', width=math.floor(width / 3), is_unicode=True)
        print_centered(ascii)
        print("")
        print_centered("Descargando")
        print_centered(Fore.LIGHTBLUE_EX + video["title"][:math.floor(width / 2)])
        os.remove(video["id"] + ".jpg")
    if index == 0:
        print(video["title"])
        inp = input(Style.RESET_ALL+Fore.LIGHTYELLOW_EX + " Nombre del archivo: " + Fore.LIGHTGREEN_EX + "\x1B[3m")
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'quiet': True,
            'no_warnings': True,
            'verbose': False,
            'outtmpl': f'downloads/{inp}.%(ext)s',

        }

        downloadingScreen()
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("")
        print_centered(Fore.LIGHTGREEN_EX + "Archivo descargado de forma exitosa.")

    elif index == 1:
        print(video["title"])
        inp = input(Fore.LIGHTYELLOW_EX + " Nombre del archivo: " + Fore.LIGHTGREEN_EX + "\x1B[3m")
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'quiet': True,
            'no_warnings': True,
            'verbose': False,
            'logger': None,
            'outtmpl': f'{inp}.mp4',

        }

        downloadingScreen()
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("")
        print_centered(Fore.LIGHTGREEN_EX + "Convirtiendo mp4 a mp3...")

        video = VideoFileClip(inp+".mp4")
        video.audio.write_audiofile("downloads/"+inp+".mp3", logger=None, bitrate="320k")
        os.remove(inp+".mp4")

        print("")
        print_centered(Fore.LIGHTGREEN_EX + "Archivo descargado de forma exitosa.")


    elif index == 2:
        busqueda(inp)


def busqueda(inp):
    if inp.startswith("https://www.youtube.com/watch?v="):
            v = Video.getInfo(inp)
            print(v)
            title = "Busqueda: " + inp
            indexes = [v, "Volver"]
            options = ["🎥 " + v["title"][:75] + (v["title"][75:] and '..') + " ⧙ ⟦" + v["channel"]["name"] + "⟧", "Volver"]
            option, index = pick(options, title, indicator='>')
            if indexes[index] == "Volver":
                start()
            else:
                os.system('clear')
                print("")
                print(" Cargando...")
                loadVideo(inp, inp, indexes[index])
    else:
        try:
            title = "Busqueda: " + inp
            videosSearch = VideosSearch(inp, limit=80)
            options = []
            indexes = []
            videos = []

            for v in videosSearch.result()["result"]:
                symbol = "🎵" if v["type"] == "🎥" else "🎵"
                options.append(
                    symbol +
                    " " + v["title"][:75] + (v["title"][75:] and '..') + " ⧙ ⟦" + v["channel"]["name"] + "⟧ ⟦" +
                    v["duration"] + "⟧"
                )
                videos.append(v)
                indexes.append(v["link"])
            options.append("Volver")
            indexes.append("Volver")

            option, index = pick(options, title, indicator='>')
            if indexes[index] == "Volver":
                start()
            else:
                os.system('clear')
                print("")
                print(" Cargando...")
                loadVideo(indexes[index], inp, videos[index])
        except Exception as e:
            os.system('clear')
            print("")
            print(" " + Fore.LIGHTRED_EX + Style.BRIGHT + "Advertencia: " + Style.RESET_ALL + Fore.LIGHTRED_EX + str(e))
            start(clear=False)

def start(clear=True):
    if clear:
        os.system('clear')
        print("")
    inp = input(Fore.LIGHTYELLOW_EX + " Busqueda de video: " + Fore.LIGHTGREEN_EX + "\x1B[3m")
    busqueda(inp)

start()
