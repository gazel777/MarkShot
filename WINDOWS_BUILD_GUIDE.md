# Windows インストーラービルドガイド

## 必要なファイル（Windowsに持っていくもの）

### 最小構成（これだけでOK）

```
MarkShot.py          # 本体スクリプト（必須）
VERSION.txt          # バージョン情報
```

### 推奨構成（ドキュメント含む）

```
MarkShot.py
VERSION.txt
README.md
CHANGELOG.md
SPEC.md
```

---

## Windows側で作成するもの

### 1. インストーラー（PyInstaller方式）

Windowsでは AppleScript が使えないため、PyInstaller を使用。

#### installer_gui.py

```python
#!/usr/bin/env python3
# MarkShot Installer for Windows
import os
import sys
import shutil
import tkinter as tk
from tkinter import messagebox

def get_target_path():
    appdata = os.environ.get('APPDATA', '')
    return os.path.join(appdata,
        'Blackmagic Design', 'DaVinci Resolve',
        'Fusion', 'Scripts', 'Utility')

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
            f"To use: DaVinci Resolve → Workspace → Scripts → MarkShot")
    except Exception as e:
        messagebox.showerror("Error", f"Installation failed:\n{e}")

def main():
    root = tk.Tk()
    root.title("MarkShot Installer")
    root.geometry("400x200")
    root.resizable(False, False)

    label = tk.Label(root, text="MarkShot Installer", font=("Arial", 16))
    label.pack(pady=20)

    info = tk.Label(root, text="Click Install to add MarkShot to DaVinci Resolve")
    info.pack(pady=10)

    btn = tk.Button(root, text="Install", command=lambda: [install(), root.destroy()],
                    width=20, height=2)
    btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
```

#### uninstaller_gui.py

```python
#!/usr/bin/env python3
# MarkShot Uninstaller for Windows
import os
import tkinter as tk
from tkinter import messagebox

def get_target_path():
    appdata = os.environ.get('APPDATA', '')
    return os.path.join(appdata,
        'Blackmagic Design', 'DaVinci Resolve',
        'Fusion', 'Scripts', 'Utility', 'MarkShot.py')

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
    root.title("MarkShot Uninstaller")
    root.geometry("400x200")
    root.resizable(False, False)

    label = tk.Label(root, text="MarkShot Uninstaller", font=("Arial", 16))
    label.pack(pady=20)

    info = tk.Label(root, text="Click Uninstall to remove MarkShot")
    info.pack(pady=10)

    btn = tk.Button(root, text="Uninstall", command=lambda: [uninstall(), root.destroy()],
                    width=20, height=2)
    btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## ビルド手順（Windows側）

### 1. 環境準備

```cmd
pip install pyinstaller
```

### 2. ビルドスクリプト作成

#### build_windows.bat

```batch
@echo off
echo ========================================
echo Building MarkShot Installer for Windows
echo ========================================

REM Build Installer
pyinstaller --onefile --windowed ^
    --name=MarkShotInstaller ^
    --add-data="MarkShot.py;." ^
    installer_gui.py

REM Build Uninstaller
pyinstaller --onefile --windowed ^
    --name=MarkShotUninstaller ^
    uninstaller_gui.py

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo Output: dist\MarkShotInstaller.exe
echo         dist\MarkShotUninstaller.exe
pause
```

### 3. 実行

```cmd
build_windows.bat
```

### 4. 出力

```
dist\
├── MarkShotInstaller.exe    # インストーラー
└── MarkShotUninstaller.exe  # アンインストーラー
```

---

## 配布パッケージ作成

```
MarkShot-v1.2.0-Windows\
├── MarkShotInstaller.exe
├── MarkShotUninstaller.exe
└── README.txt
```

ZIPに圧縮して配布。

---

## 注意点

1. **PyInstallerはクロスコンパイル非対応**
   - Windows用はWindowsでビルドが必要
   - macOS用はmacOSでビルドが必要

2. **Windows Defender警告**
   - 未署名のexeは警告が出る
   - ユーザーに「詳細情報」→「実行」を案内

3. **テストチェックリスト**
   - [ ] インストーラーが起動する
   - [ ] DaVinci Resolveのスクリプトフォルダにコピーされる
   - [ ] DaVinci ResolveでMarkShotが表示される
   - [ ] 書き出しが正常に動作する
   - [ ] アンインストーラーでファイルが削除される

---

## ファイル一覧（Windows環境用）

```
Windows作業フォルダ\
├── MarkShot.py              # macOSから持ってくる
├── VERSION.txt              # macOSから持ってくる
├── installer_gui.py         # 上記のコードで作成
├── uninstaller_gui.py       # 上記のコードで作成
└── build_windows.bat        # 上記のコードで作成
```
