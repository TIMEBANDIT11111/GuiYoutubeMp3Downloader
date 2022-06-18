import tkinter as tk
from tkinter import ttk
from tkinter import *
from pytube import Playlist
import os
from pytube import YouTube
import threading
root = tk.Tk()
root.geometry("580x360")
name_var = tk.StringVar()

newpath = 'Downloads'
if not os.path.exists(newpath):
    os.makedirs(newpath) #creates directory for mp3 files if doesn't exist

def clicked():#used to create threads so tkinter doesn't crash while download in progress and user can make multiple downloads at the same time
    threading.Thread(target=download).start()

def write(*message, end="\n", sep=" "):#used to write informations to first text area
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    Console.see(tk.END)
    Console.insert(INSERT, text)

def write2(*message, end="\n", sep=" "):#used to write informations to second text area
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    Console2.see(tk.END)
    Console2.insert(INSERT, text)

def download():
    p = str(name_var.get())#gets link from user input area
    name_var.set("")
    write(f"[DOWNLOADING] {p}")
    if "playlist" in p:#checks if input is playlist or song link
        p = Playlist(p)
        for video in p.videos:
            try:#downloading every song in playlist to Downloads folder
                yt = YouTube(video.watch_url)
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(newpath)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                write2(f"[SUCCESFUL] {video.title}")
            except:
                write2(f"[ERROR](video might be age restricted)")
    else:
        try:#downloading song to Downloads folder
            yt = YouTube(p)
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(newpath)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            write2(f"[SUCCESFUL] {video.title}")
        except:
            write2(f"[ERROR](video might be age restricted)")

#user entry and download button
name_label = tk.Label(root, text='Song or Playlist url', font=('calibre', 10, 'bold'))
name_entry = tk.Entry(root,width=50, textvariable=name_var, font=('calibre', 10, 'normal'))
sub_btn = ttk.Button(root, text='DOWNLOAD', command=lambda:clicked())
name_label.grid(row=0, column=0)
name_entry.grid(row=0, column=1)
sub_btn.grid(row=0, column=2)

#first text output area
Console = Text()
Console.config(height=10, width=70,font=("Arial",9))
Console.grid(row=2, column=0,columnspan=3,pady=5)

#second text output area
Console2 = Text()
Console2.config(height=10, width=70,font=("Arial",9))
Console2.grid(row=3, column=0,columnspan=3,rowspan=2,pady=5)

root.title('Youtube mp3 Downloader')
root.mainloop()
