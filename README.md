# MarkShot - DaVinci Resolve Marker Frame Export

A script that automatically exports frames from marker positions on your DaVinci Resolve timeline.

**Version**: 1.3.3

> 🇯🇵 [日本語はこちら](README-JP.md)

## Features

- Automatically detects **all markers** on the timeline
- Exports each marker position as a **still image**
- **Timecode in filenames** — automatically appended
- **Data burn-in support** — bake in timecode, clip names, etc. set in DaVinci Resolve
- **DaVinci Resolve Free version supported** (v1.3.0+)
- **Duplicate filename handling** — auto-numbering with `-2`, `-3` when files already exist (v1.3.3+)

**Studio only:**
- Output format selection (JPEG / PNG / TIFF)
- Marker color filtering

## Requirements

- **DaVinci Resolve 17.4+** (Free or Studio)
- **macOS 10.15+** or **Windows 10+**

---

## Free vs Studio

| Feature | Studio | Free |
|---------|--------|------|
| Export stills from marker positions | ✅ | ✅ |
| Data burn-in | ✅ | ✅ |
| Output format selection | JPEG/PNG/TIFF | JPEG only |
| Marker color filter | ✅ | − |

**Note for Free version:**
- No settings dialog — runs with default settings.

---

## Installation

### Windows (Installer)

1. Download `MarkShotInstaller_v1.3.3.exe` from [Releases](../../releases)
2. Run the downloaded exe
3. Click "Install"
4. Done

### macOS (Installer)

1. Download `MarkShot-v1.3.3-macOS.dmg` from [Releases](../../releases)
2. Double-click the DMG to mount
3. Double-click `Install MarkShot.app`
4. Click "Install"
5. Done

### Manual Install

Copy `MarkShot.py` to:

**Windows:**
```
%APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility\
```

**macOS:**
```
~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/
```

---

## Uninstall

### Windows
- Run `MarkShotUninstaller.exe`

### macOS
- Run `Uninstall MarkShot.app` from the DMG

### Manual Uninstall

Delete the following file:

**Windows:**
1. Open in Explorer:
   ```
   %APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility
   ```
2. Delete `MarkShot.py`

**macOS:**
1. In Finder, press `Shift + Command + G` (Go to Folder)
2. Enter:
   ```
   ~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility
   ```
3. Delete `MarkShot.py`

---

## Usage

### Studio

1. Open DaVinci Resolve with a project and timeline
2. Add markers on the timeline (shortcut: `M`)
3. Go to `Workspace` → `Scripts` → `MarkShot`
4. In the settings dialog, choose:
   - **File Format**: JPEG / PNG / TIFF
   - **Marker Color**: All / specific color
   - **Include Data Burn-in**: whether to bake in timecode overlay
5. Select an output folder
6. When done, the folder opens automatically

### Free Version

1. Open DaVinci Resolve with a project and timeline
2. Add markers on the timeline (shortcut: `M`)
3. Go to `Workspace` → `Scripts` → `MarkShot`
4. Select an output folder
5. When done, the folder opens automatically

**First launch (Free version only):**
On the first run, a dialog asks "Are you using Studio version?" — select "No". The first export may produce incorrect stills. **Run the script a second time** and it will work correctly from then on.

**Note:** The Free version has no settings dialog — it uses default settings (JPEG, all markers, data burn-in ON).

---

## Data Burn-in

Bake in timecode, filenames, and other overlays set in DaVinci Resolve.

**Setup:**
1. In DaVinci Resolve, go to `Workspace` → `Data Burn-in`
2. Configure what to display (timecode, etc.)
3. Run MarkShot

**Studio:** ON/OFF selectable (default: ON)
**Free:** Always ON

---

## Output Files

Filename format:
```
[ProjectName]_[HH_MM_SS_FF].jpg
```

Example: `MyMovie_00_01_23_15.jpg`

---

## Troubleshooting

### MarkShot doesn't appear in the menu

- Restart DaVinci Resolve
- Verify the file is in the correct location
- Go to `Preferences` → `System` → `General` → set "External scripting using" to "Local"

### "Cannot connect to DaVinci Resolve" error

- Make sure DaVinci Resolve is running
- Open the Fusion page (Free version)
- Verify you're running the script correctly from the console

### "Unidentified developer" warning (macOS)

1. Go to System Settings → Privacy & Security
2. Click "Open Anyway"

### Images not exporting correctly

- Confirm markers exist on the timeline
- Make sure a project and timeline are open

---

## Also by FrameTools

### [S2S (Slice2Storyboard)](https://oneframestudio.net/s2s/en/) — Video → Storyboard in Seconds

MarkShot extracts frames from markers you place. **S2S goes further** — drop any video and it automatically detects every cut, generating a complete storyboard.

- **Automatic scene detection** — no manual markers needed
- **Multiple export formats** — Excel, PDF, ZIP
- **Layout options** — vertical/horizontal grids, multiple aspect ratios

Great for studying film editing structure, building storyboards from reference footage, or extracting key frames at scale.

**[Try S2S free → oneframestudio.net/s2s/en/](https://oneframestudio.net/s2s/en/)**

---

## License

MIT License

## Author

Hiro / FrameTools
