import subprocess
import sys

def install_dependencies():
    print("🔧 Installing dependencies...")
    required_packages = ['pynput', 'keyboard']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")

def download_and_run():
    print("\n🚀 Starting Sneaky Clicker...")

    code = '''
import tkinter as tk
from tkinter import ttk
import threading
import time
import keyboard
from pynput.mouse import Controller, Button

class SneakyClicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sneaky Clicker")
        self.root.geometry("300x280")
        self.root.configure(bg='#121212')
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)

        # Porta la finestra in primo piano anche con exec()
        self.root.lift()
        self.root.after_idle(self.root.attributes, '-topmost', False)

        self.mouse = Controller()
        self.left_click_active = False
        self.right_click_active = False
        self.left_click_key = None
        self.right_click_key = None
        self.capturing_left_key = False
        self.capturing_right_key = False
        self.left_cps = 10
        self.right_cps = 10
        self.is_dragging_left = False
        self.is_dragging_right = False
        self.left_click_thread = None
        self.right_click_thread = None
        self.left_stop_event = threading.Event()
        self.right_stop_event = threading.Event()

        self.setup_ui()
        self.setup_hotkeys()

    def setup_ui(self):
        # UI Labels e Pulsanti
        tk.Label(self.root, text="Sneaky Clicker", font=("Segoe UI", 14, "bold"), fg="#78DC78", bg="#121212").place(x=70, y=15, width=160, height=25)
        tk.Button(self.root, text="×", font=("Segoe UI", 12, "bold"), fg="#969696", bg="#121212", bd=0, command=self.close_app, activebackground="#121212", activeforeground="#FF5050").place(x=260, y=5, width=25, height=25)
        tk.Label(self.root, text="Left click", font=("Segoe UI", 10), fg="#C8C8C8", bg="#121212").place(x=30, y=65)
        tk.Label(self.root, text="Right click", font=("Segoe UI", 10), fg="#C8C8C8", bg="#121212").place(x=30, y=135)

        self.left_key_btn = tk.Button(self.root, text="none", font=("Segoe UI", 9), fg="#C8C8C8", bg="#232323", bd=1, relief="solid", command=self.capture_left_key)
        self.left_key_btn.place(x=105, y=63, width=60, height=24)
        self.right_key_btn = tk.Button(self.root, text="none", font=("Segoe UI", 9), fg="#C8C8C8", bg="#232323", bd=1, relief="solid", command=self.capture_right_key)
        self.right_key_btn.place(x=105, y=133, width=60, height=24)

        self.left_cps_label = tk.Label(self.root, text="10 CPS", font=("Segoe UI", 10, "bold"), fg="#78DC78", bg="#121212", anchor="e")
        self.left_cps_label.place(x=175, y=65, width=90, height=20)
        self.right_cps_label = tk.Label(self.root, text="10 CPS", font=("Segoe UI", 10, "bold"), fg="#78DC78", bg="#121212", anchor="e")
        self.right_cps_label.place(x=175, y=135, width=90, height=20)

        self.left_bar_canvas = tk.Canvas(self.root, width=235, height=10, bg="#232323", highlightthickness=0, cursor="hand2")
        self.left_bar_canvas.place(x=30, y=95)
        self.left_progress = self.left_bar_canvas.create_rectangle(0, 0, 78, 10, fill="#78DC78", outline="")
        self.left_bar_canvas.bind("<Button-1>", self.on_left_bar_click)
        self.left_bar_canvas.bind("<B1-Motion>", self.on_left_bar_drag)
        self.left_bar_canvas.bind("<ButtonRelease-1>", self.on_left_bar_release)

        self.right_bar_canvas = tk.Canvas(self.root, width=235, height=10, bg="#232323", highlightthickness=0, cursor="hand2")
        self.right_bar_canvas.place(x=30, y=165)
        self.right_progress = self.right_bar_canvas.create_rectangle(0, 0, 78, 10, fill="#78DC78", outline="")
        self.right_bar_canvas.bind("<Button-1>", self.on_right_bar_click)
        self.right_bar_canvas.bind("<B1-Motion>", self.on_right_bar_drag)
        self.right_bar_canvas.bind("<ButtonRelease-1>", self.on_right_bar_release)

        self.status_label = tk.Label(self.root, text="", font=("Segoe UI", 7), fg="#8C8C8C", bg="#121212")
        self.status_label.place(x=30, y=195, width=240, height=15)
        tk.Label(self.root, text="v1.5", font=("Segoe UI", 9), fg="#505050", bg="#121212").place(x=10, y=220)

    # --- Gestione CPS, click e hotkey ---
    def on_left_bar_click(self, event): self.is_dragging_left=True; self.update_left_cps(event.x)
    def on_left_bar_drag(self, event): 
        if self.is_dragging_left: self.update_left_cps(event.x)
    def on_left_bar_release(self, event): self.is_dragging_left=False
    def update_left_cps(self, x): 
        x = max(0, min(235, x))
        self.left_cps = max(1, min(30, int((x / 235.0) * 30) + 1))
        self.left_cps_label.config(text=f"{self.left_cps} CPS")
        self.left_bar_canvas.coords(self.left_progress, 0,0,int(235*(self.left_cps/30.0)),10)

    def on_right_bar_click(self, event): self.is_dragging_right=True; self.update_right_cps(event.x)
    def on_right_bar_drag(self, event): 
        if self.is_dragging_right: self.update_right_cps(event.x)
    def on_right_bar_release(self, event): self.is_dragging_right=False
    def update_right_cps(self, x): 
        x = max(0, min(235, x))
        self.right_cps = max(1, min(30, int((x / 235.0) * 30) + 1))
        self.right_cps_label.config(text=f"{self.right_cps} CPS")
        self.right_bar_canvas.coords(self.right_progress, 0,0,int(235*(self.right_cps/30.0)),10)

    def capture_left_key(self):
        self.left_key_btn.config(text="Press...", bg="#323232")
        self.capturing_left_key=True
        self.status_label.config(text="Press a key for left click...")
    def capture_right_key(self):
        self.right_key_btn.config(text="Press...", bg="#323232")
        self.capturing_right_key=True
        self.status_label.config(text="Press a key for right click...")

    def on_key_press(self, event):
        if self.capturing_left_key:
            self.left_click_key=event.name
            self.left_key_btn.config(text=event.name.upper(), bg="#232323")
            self.status_label.config(text=f"Left key set: {event.name.upper()}")
            self.capturing_left_key=False
            keyboard.on_press_key(event.name, self.toggle_left_click,suppress=False)
        elif self.capturing_right_key:
            self.right_click_key=event.name
            self.right_key_btn.config(text=event.name.upper(), bg="#232323")
            self.status_label.config(text=f"Right key set: {event.name.upper()}")
            self.capturing_right_key=False
            keyboard.on_press_key(event.name, self.toggle_right_click,suppress=False)

    def setup_hotkeys(self):
        keyboard.on_press(self.on_key_press)

    def toggle_left_click(self,event=None):
        if self.capturing_left_key: return
        self.left_click_active=not self.left_click_active
        if self.left_click_active:
            self.left_key_btn.config(bg="#50B450")
            self.status_label.config(text="LEFT CLICKING ACTIVE!", fg="#78DC78")
            self.left_stop_event.clear()
            self.left_click_thread=threading.Thread(target=self.left_click_loop,daemon=True)
            self.left_click_thread.start()
        else:
            self.left_key_btn.config(bg="#232323")
            self.status_label.config(text="Left clicking stopped", fg="#8C8C8C")
            self.left_stop_event.set()

    def toggle_right_click(self,event=None):
        if self.capturing_right_key: return
        self.right_click_active=not self.right_click_active
        if self.right_click_active:
            self.right_key_btn.config(bg="#50B450")
            self.status_label.config(text="RIGHT CLICKING ACTIVE!", fg="#78DC78")
            self.right_stop_event.clear()
            self.right_click_thread=threading.Thread(target=self.right_click_loop,daemon=True)
            self.right_click_thread.start()
        else:
            self.right_key_btn.config(bg="#232323")
            self.status_label.config(text="Right clicking stopped", fg="#8C8C8C")
            self.right_stop_event.set()

    def left_click_loop(self):
        while not self.left_stop_event.is_set():
            self.mouse.click(Button.left,1)
            time.sleep(1.0/self.left_cps)

    def right_click_loop(self):
        while not self.right_stop_event.is_set():
            self.mouse.click(Button.right,1)
            time.sleep(1.0/self.right_cps)

    def close_app(self):
        self.left_stop_event.set()
        self.right_stop_event.set()
        keyboard.unhook_all()
        self.root.quit()
        self.root.destroy()

    def run(self):
        print("Sneaky Clicker v1.5 started successfully!")
        print("Drag the CPS bars to adjust the click speed!")
        self.root.mainloop()

if __name__=="__main__":
    app=SneakyClicker()
    app.run()
'''

    exec(code)

if __name__ == "__main__":
    print("="*50)
    print("    SNEAKY CLICKER - AUTO INSTALLER")
    print("="*50)
    
    install_dependencies()
    download_and_run()
