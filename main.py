import tkinter as tk
from tkinter import filedialog
from pygame import mixer
import os
import time
import threading

# Node class for the doubly linked list
class SongNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

# Doubly linked list class to manage songs
class DoublyLinkedSongList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def append(self, data):
        new_node = SongNode(data)
        if not self.head:
            self.head = self.tail = new_node
            self.current = self.head
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def next_song(self):
        if self.current and self.current.next:
            self.current = self.current.next
        return self.current.data if self.current else None

    def prev_song(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        return self.current.data if self.current else None

    def current_song(self):
        return self.current.data if self.current else None

    def set_current(self, index):
        temp = self.head
        for _ in range(index):
            if temp.next:
                temp = temp.next
        self.current = temp

# Audio player app class
class AudioPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Player")
        self.root.geometry("400x300")
        mixer.init()

        self.song_list = DoublyLinkedSongList()
        self.song_length = 0
        self.is_paused = False

        self.create_widgets()
        self.load_songs()

        self.update_slider = True

    def load_songs(self):
        music_dir = "music/"
        self.songs = []
        for file in os.listdir(music_dir):
            if file.endswith(".mp3"):
                full_path = os.path.join(music_dir, file)
                self.song_list.append(full_path)
                self.songs.append(file)
        for song in self.songs:
            self.song_listbox.insert(tk.END, song)

    def create_widgets(self):
        self.song_listbox = tk.Listbox(self.root, width=50)
        self.song_listbox.pack(pady=10)
        self.song_listbox.bind('<Double-1>', self.play_selected_song)

        self.song_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=300, command=self.seek_song)
        self.song_slider.pack(pady=10)

        btn_play = tk.Button(self.root, text="Play", command=self.play_song)
        btn_play.pack(pady=5)

        btn_pause = tk.Button(self.root, text="Pause", command=self.pause_song)
        btn_pause.pack(pady=5)

        btn_next = tk.Button(self.root, text="Next", command=self.next_song)
        btn_next.pack(pady=5)

        btn_prev = tk.Button(self.root, text="Previous", command=self.prev_song)
        btn_prev.pack(pady=5)

        btn_stop = tk.Button(self.root, text="Stop", command=self.stop_song)
        btn_stop.pack(pady=5)

    def play_selected_song(self, event):
        index = self.song_listbox.curselection()[0]
        self.song_list.set_current(index)
        self.play_song()

    def play_song(self):
        song = self.song_list.current_song()
        if song:
            mixer.music.load(song)
            mixer.music.play()
            self.is_paused = False
            self.song_length = mixer.Sound(song).get_length()
            self.song_slider.config(to=int(self.song_length))
            threading.Thread(target=self.update_slider_position).start()

    def pause_song(self):
        if self.is_paused:
            mixer.music.unpause()
            self.is_paused = False
        else:
            mixer.music.pause()
            self.is_paused = True

    def stop_song(self):
        mixer.music.stop()
        self.update_slider = False

    def next_song(self):
        song = self.song_list.next_song()
        if song:
            mixer.music.load(song)
            mixer.music.play()
            self.is_paused = False
            self.song_length = mixer.Sound(song).get_length()
            self.song_slider.config(to=int(self.song_length))
            threading.Thread(target=self.update_slider_position).start()

    def prev_song(self):
        song = self.song_list.prev_song()
        if song:
            mixer.music.load(song)
            mixer.music.play()
            self.is_paused = False
            self.song_length = mixer.Sound(song).get_length()
            self.song_slider.config(to=int(self.song_length))
            threading.Thread(target=self.update_slider_position).start()

    def seek_song(self, val):
        mixer.music.set_pos(float(val))

    def update_slider_position(self):
        while mixer.music.get_busy() and self.update_slider:
            current_pos = mixer.music.get_pos() / 1000
            self.song_slider.set(current_pos)
            time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayerApp(root)
    root.mainloop()
