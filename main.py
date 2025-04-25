import tkinter as tk
from PIL import Image, ImageTk
import os
import json
import pygame
import random

# 初始化語音模組
pygame.mixer.init()

# 載入設定
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# 主視窗設定
root = tk.Tk()
root.title("Gura Live 假皮")
root.geometry(f"{config['width']}x{config['height']}+{config['x']}+{config['y']}")
root.overrideredirect(True)
root.wm_attributes("-topmost", 1)
root.wm_attributes("-transparentcolor", config["transparent_color"])

# 載入圖片
def load_image(filename):
    path = os.path.join("assets", filename)
    return ImageTk.PhotoImage(Image.open(path).resize((config['width'], config['height']), Image.ANTIALIAS))

bg_img = load_image("gura_idle.png")

# 嘗試載入嘴型圖（可選）
try:
    mouth_a = load_image("mouth_a.png")
    mouth_b = load_image("mouth_b.png")
    use_mouth = True
except:
    use_mouth = False

# 初始圖層
label = tk.Label(root, image=bg_img, bg=config["transparent_color"])
label.place(x=0, y=0)

# 漂浮動畫
def float_animation():
    y = random.randint(-2, 2)
    x = root.winfo_x()
    root.geometry(f"+{x}+{config['y'] + y}")
    root.after(300, float_animation)

# 嘴型動畫（如果有的話）
def animate_mouth():
    if not use_mouth:
        return
    def swap(n):
        if n <= 0:
            label.config(image=bg_img)
            return
        label.config(image=mouth_b if n % 2 == 0 else mouth_a)
        root.after(200, swap, n - 1)
    swap(6)

# 播放語音
def play_voice():
    voices = os.listdir("voice")
    if voices:
        file = random.choice(voices)
        pygame.mixer.music.load(os.path.join("voice", file))
        pygame.mixer.music.play()
        animate_mouth()

# 點擊播放語音
label.bind("<Button-1>", lambda e: play_voice())

# 拖曳功能
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

label.bind("<Button-1>", start_move)
label.bind("<ButtonRelease-1>", stop_move)
label.bind("<B1-Motion>", do_move)

float_animation()
root.mainloop()
