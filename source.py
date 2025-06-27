import tkinter as tk
import random
import time
import threading
import winsound
import keyboard
import ctypes
import os
import sys

try:
    p = sys._MEIPASS
except:
    p = os.path.abspath(".")

os.chdir(p)

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

code_buffer = []
exit_code = [1, 2, 1, 3]
exit_flag = False

def play_sound():
    if os.path.exists('meme.wav'):

        try:
            winsound.PlaySound('meme.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        except:
            pass
    else:
        pass

def on_key_event(e):
    global exit_flag
    if e.event_type == keyboard.KEY_DOWN and e.name.isdigit():
        code_buffer.append(int(e.name))
        if len(code_buffer) > len(exit_code):
            code_buffer.pop(0)
        if code_buffer == exit_code:
            exit_flag = True

keyboard.hook(on_key_event)

root = tk.Tk()
root.withdraw()

windows = []

color_options = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#FFA500"]

def create_window():
    win = tk.Toplevel()
    win.overrideredirect(True)
    win.attributes('-topmost', True)
    win_width = random.randint(300, 500)
    win_height = random.randint(200, 400)
    x = random.randint(0, screensize[0] - 100)
    y = random.randint(0, screensize[1] - 100)
    win.geometry(f"{win_width}x{win_height}+{x}+{y}")
    bg_color = random.choice(color_options)
    text_color = "#000000" if bg_color in ["#FF0000", "#00FF00", "#0000FF"] else "#FFFFFF"
    try:
        img = tk.PhotoImage(file='zelenskiy.png').subsample(random.randint(1, 3))
        label = tk.Label(win, image=img, text='Вийди звідси РОЗБІЙНИК!', compound='top', font=('Arial', random.randint(20, 30)), fg=text_color, bg=bg_color)
        label.image = img
    except:
        label = tk.Label(win, text='Вийди звідси РОЗБІЙНИК!', font=('Arial', random.randint(20, 30)), fg=text_color, bg=bg_color)
    label.pack(expand=True, fill='both')
    btn_text = random.choice(["Выход", "Закрити", "Вихід", "Close"])
    btn = tk.Button(win, text=btn_text, width=10, height=2, command=lambda w=win: block_mouse(w), bg="#FFD700")
    btn.pack(pady=10)
    windows.append((win, label, img if 'img' in locals() else None))
    sound_thread = threading.Thread(target=play_sound)
    sound_thread.daemon = True
    sound_thread.start()

def block_mouse(win):
    try:
        from ctypes import windll, Structure, c_long, byref
        class POINT(Structure): _fields_ = [("x", c_long), ("y", c_long)]
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        orig_x, orig_y = pt.x, pt.y
        for _ in range(3):
            time.sleep(0.3)
            ctypes.windll.user32.SetCursorPos(orig_x, orig_y)
    except:
        pass

for _ in range(100):
    create_window()

def update_windows():
    while not exit_flag:
        for win, label, img in windows:
            if exit_flag:
                break
            try:
                label.config(font=('Arial', random.randint(20, 30)))
                win.attributes('-alpha', random.choice([0.8, 0.9, 1.0]))
            except:
                pass
            win.update()
        if len(windows) > 200:
            old_windows = windows[:100]
            for win, _, _ in old_windows:
                win.destroy()
            del windows[:100]
            for _ in range(50):
                create_window()
        time.sleep(0.1)

threading.Thread(target=update_windows, daemon=True).start()

root.mainloop()

for win, _, _ in windows:
    win.destroy()
keyboard.unhook_all()