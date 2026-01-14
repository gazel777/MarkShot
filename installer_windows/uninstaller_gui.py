#!/usr/bin/env python3
# MarkShot Uninstaller for Windows
# Version 1.3.2

VERSION = "1.3.2"

import os
import tkinter as tk
from tkinter import messagebox

def get_target_path():
    appdata = os.environ.get('APPDATA', '')
    return os.path.join(appdata,
        'Blackmagic Design', 'DaVinci Resolve',
        'Support', 'Fusion', 'Scripts', 'Utility', 'MarkShot.py')

def uninstall():
    target = get_target_path()

    if not os.path.exists(target):
        messagebox.showinfo("Info", "MarkShot is not installed.")
        return

    try:
        os.remove(target)
        messagebox.showinfo("Success", "MarkShot has been uninstalled.")
    except Exception as e:
        messagebox.showerror("Error", f"Uninstall failed:\n{e}")

def main():
    root = tk.Tk()
    root.title(f"MarkShot Uninstaller v{VERSION}")
    root.geometry("400x220")
    root.resizable(False, False)

    label = tk.Label(root, text="MarkShot Uninstaller", font=("Arial", 16))
    label.pack(pady=10)

    version_label = tk.Label(root, text=f"Version {VERSION}", font=("Arial", 10), fg="gray")
    version_label.pack()

    info = tk.Label(root, text="Click Uninstall to remove MarkShot")
    info.pack(pady=10)

    btn = tk.Button(root, text="Uninstall", command=lambda: [uninstall(), root.destroy()],
                    width=20, height=2)
    btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
