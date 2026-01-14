#!/usr/bin/env python3
# MarkShot Installer for Windows
# Version 1.3.3

VERSION = "1.3.3"

import os
import sys
import shutil
import tkinter as tk
from tkinter import messagebox

def get_target_path():
    appdata = os.environ.get('APPDATA', '')
    return os.path.join(appdata,
        'Blackmagic Design', 'DaVinci Resolve',
        'Support', 'Fusion', 'Scripts', 'Utility')

def install():
    target_dir = get_target_path()

    # Create directory if not exists
    os.makedirs(target_dir, exist_ok=True)

    # Get source file (bundled with exe)
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)

    source = os.path.join(base_path, 'MarkShot.py')
    target = os.path.join(target_dir, 'MarkShot.py')

    try:
        shutil.copy2(source, target)
        messagebox.showinfo("Success",
            f"MarkShot installed successfully!\n\n"
            f"Location:\n{target}\n\n"
            f"To use:\n"
            f"1. Open DaVinci Resolve\n"
            f"2. Go to Fusion page\n"
            f"3. Open Console (Workspace > Console)\n"
            f"4. Run: exec(open(r'{target}').read())")
    except Exception as e:
        messagebox.showerror("Error", f"Installation failed:\n{e}")

def main():
    root = tk.Tk()
    root.title(f"MarkShot Installer v{VERSION}")
    root.geometry("400x270")
    root.resizable(False, False)

    label = tk.Label(root, text=f"MarkShot Installer", font=("Arial", 16))
    label.pack(pady=10)

    version_label = tk.Label(root, text=f"Version {VERSION}", font=("Arial", 10), fg="gray")
    version_label.pack()

    info = tk.Label(root, text="Marker Frame Export Tool for DaVinci Resolve\n\nClick Install to add MarkShot")
    info.pack(pady=10)

    btn = tk.Button(root, text="Install", command=lambda: [install(), root.destroy()],
                    width=20, height=2)
    btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
