# YouTube & Twitter Downloader GUI (Modern UI)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import ttkbootstrap as tb
import re

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Downloader - Modern UI")
        self.root.geometry("750x450")
        self.style = tb.Style("flatly")

        self.platform = tk.StringVar(value="YouTube")
        self.url = tk.StringVar()
        self.subtitle_lang = tk.StringVar()
        self.audio_only = tk.BooleanVar()

        self.url.trace_add('write', lambda *args: self.on_url_change())

        self.download_path = tk.StringVar()
        self.set_default_download_path()

        self.create_widgets()

    def set_default_download_path(self):
        platform = self.platform.get()
        platform_folder = f"downloads_{platform.lower()}"
        path = os.path.join(os.getcwd(), platform_folder)
        os.makedirs(path, exist_ok=True)
        self.download_path.set(path)

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Platform:").grid(row=0, column=0, sticky='w')
        platform_menu = ttk.Combobox(frame, textvariable=self.platform, values=["YouTube", "Twitter"], state='readonly', width=10)
        platform_menu.grid(row=0, column=1, sticky='w')
        platform_menu.bind('<<ComboboxSelected>>', lambda e: self.on_platform_change())

        ttk.Label(frame, text="URL:").grid(row=1, column=0, sticky='w')
        ttk.Entry(frame, textvariable=self.url, width=60).grid(row=1, column=1, columnspan=2, pady=5, sticky='ew')

        ttk.Label(frame, text="Subtitle Language:").grid(row=2, column=0, sticky='w')
        self.subtitle_dropdown = ttk.Combobox(frame, textvariable=self.subtitle_lang, values=["", "en", "hi"], width=10)
        self.subtitle_dropdown.grid(row=2, column=1, sticky='w')
        self.subtitle_dropdown.set("")

        self.audio_chk = ttk.Checkbutton(frame, text="Audio Only (MP3)", variable=self.audio_only)
        self.audio_chk.grid(row=2, column=2, sticky='w')

        ttk.Label(frame, text="Download Location:").grid(row=3, column=0, sticky='w', pady=(10,0))
        ttk.Entry(frame, textvariable=self.download_path, width=50).grid(row=3, column=1, pady=(10,0))
        ttk.Button(frame, text="Browse", command=self.browse_folder).grid(row=3, column=2, pady=(10,0))

        ttk.Button(frame, text="Download", bootstyle='success', command=self.start_download).grid(row=4, column=1, pady=20)

        self.progress = ttk.Progressbar(frame, length=500, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=5)

        self.status_label = ttk.Label(frame, text="Ready")
        self.status_label.grid(row=6, column=0, columnspan=3)

        self.error_box = tk.Text(frame, height=4, wrap='word', state='disabled', bg='#f8f9fa')
        self.error_box.grid(row=7, column=0, columnspan=3, pady=(10, 0), sticky='nsew')

        self.update_visibility()
        self.platform.trace_add('write', lambda *args: self.update_visibility())

    def on_platform_change(self):
        self.set_default_download_path()
        self.update_visibility()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path.set(folder)

    def on_url_change(self):
        pass

    def update_visibility(self):
        is_youtube = self.platform.get() == "YouTube"
        enable = 'readonly' if is_youtube else 'disabled'
        self.subtitle_dropdown.configure(state=enable)
        self.audio_chk.configure(state='normal' if is_youtube else 'disabled')

    def start_download(self):
        self.progress.start()
        self.status_label.config(text="Starting download...")
        threading.Thread(target=self.download).start()

    def get_video_count(self, url):
        try:
            cmd = ["yt-dlp", "--flat-playlist", "--print", "%(id)s", url]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            video_ids = result.stdout.strip().split("\n")
            return len(video_ids)
        except:
            return 1

    def download(self):
        url = self.url.get()
        folder = self.download_path.get()
        subtitle = self.subtitle_lang.get()
        platform = self.platform.get()

        if not url or not folder:
            self.show_error("URL and Download Path are required")
            return

        profile_name_match = re.search(r"(?:youtube\\.com|twitter\\.com)/(?:c/|user/|channel/|@)?([\w\\-\.]+)", url)
        profile_name = profile_name_match.group(1) if profile_name_match else "media"

        profile_folder = os.path.join(folder, profile_name)
        os.makedirs(profile_folder, exist_ok=True)

        output_template = os.path.join(profile_folder, "%(title)s.%(ext)s")
        cmd = ["yt-dlp", url, "--output", output_template, "--user-agent", "Mozilla/5.0"]

        if platform == "YouTube":
            if subtitle in ["en", "hi"]:
                cmd += ["--sub-langs", subtitle, "--write-subs", "--write-auto-sub", "--convert-subs", "srt"]
            cmd += ["--write-thumbnail"]
            if self.audio_only.get():
                cmd += ["-f", "bestaudio", "--extract-audio", "--audio-format", "mp3"]
            else:
                cmd += ["-f", "bestvideo+bestaudio"]

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                if "Destination:" in line:
                    self.status_label.config(text="Downloading...")
                self.root.update()
            self.progress.stop()
            self.status_label.config(text="Download complete.")
            messagebox.showinfo("Success", "Download completed successfully.")
        except Exception as e:
            self.progress.stop()
            self.show_error(str(e))

    def show_error(self, msg):
        self.status_label.config(text="Error occurred.")
        self.error_box.config(state='normal')
        self.error_box.delete("1.0", tk.END)
        self.error_box.insert(tk.END, msg)
        self.error_box.config(state='disabled')
        messagebox.showerror("Error", msg)

if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = DownloaderApp(root)
    root.mainloop()
