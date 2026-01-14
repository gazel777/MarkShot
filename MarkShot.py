#!/usr/bin/env python3
# MarkShot.py
# DaVinci Resolve Marker Frame Export Tool
# v1.3.3 - Auto-numbering for duplicate filenames (-2, -3, etc.)

import os
import glob
import time
import subprocess
import platform

print("=" * 60)
print("MarkShot - Marker Frame Export Tool v1.3.3")
print("=" * 60)

# Try to get Resolve using multiple methods
resolve = None

# Method 1: bmd (Studio version, Console)
try:
    resolve = bmd.scriptapp("Resolve")
except NameError:
    pass

# Method 2: app variable (Free version support)
if not resolve:
    try:
        resolve = app.GetResolve()
    except NameError:
        pass

# Method 3: DaVinciResolveScript (external execution)
if not resolve:
    try:
        import DaVinciResolveScript
        resolve = DaVinciResolveScript.scriptapp("Resolve")
    except ImportError:
        pass

if not resolve:
    print("ERROR: Cannot connect to DaVinci Resolve API")
    raise SystemExit("Please run from DaVinci Resolve")

print("OK: Connected to DaVinci Resolve")

# Get project
pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()

if not project:
    print("ERROR: No project is open")
    raise SystemExit("Please open a project first")

project_name = project.GetName()
print(f"OK: Project: {project_name}")

# Get timeline
timeline = project.GetCurrentTimeline()

if not timeline:
    print("ERROR: No timeline is open")
    raise SystemExit("Please open a timeline first")

timeline_name = timeline.GetName()
print(f"OK: Timeline: {timeline_name}")

# Timeline info
start_frame = timeline.GetStartFrame()
start_tc = timeline.GetStartTimecode()
fps_str = timeline.GetSetting('timelineFrameRate')

fps_map = {
    "23.976": 23.976,
    "24": 24.0,
    "25": 25.0,
    "29.97": 29.97,
    "30": 30.0,
    "50": 50.0,
    "59.94": 59.94,
    "60": 60.0
}
fps = fps_map.get(fps_str, float(fps_str))

print(f"  Start TC: {start_tc}")
print(f"  FPS: {fps}")

# Get markers
markers = timeline.GetMarkers()

if not markers:
    print("WARNING: No markers found")
    print("   Please add markers to timeline (press M)")
    raise SystemExit()

marker_count = len(markers)
print(f"OK: Markers: {marker_count}")
print("-" * 60)

# Gallery setup
gallery = project.GetGallery()
album = gallery.GetCurrentStillAlbum()

# Get Fusion object for UI
fusion = resolve.Fusion()

# ============================================================
# Settings Dialog
# ============================================================

# Default settings
selected_format = "JPEG"
selected_color = "All"
use_burnin = True  # Default ON (auto-fallback for Free version)

# Available options
FORMAT_OPTIONS = ["JPEG", "PNG", "TIFF"]

# Get actual marker colors from timeline
marker_colors_in_timeline = set()
for marker_info in markers.values():
    color = marker_info.get('color')
    if color:
        marker_colors_in_timeline.add(color)

# Build color options: "All" + colors actually present in timeline
COLOR_OPTIONS = ["All"] + sorted(list(marker_colors_in_timeline))

# Format mapping for ExportStills API
FORMAT_MAP = {"PNG": "png", "JPEG": "jpg", "TIFF": "tif"}

# Try to show settings dialog using UIManager
try:
    ui = fusion.UIManager
    disp = bmd.UIDispatcher(ui)

    # Dialog result storage
    dialog_result = {"ok": False, "format": "JPEG", "color": "All", "burnin": True}

    # Create dialog window
    win = disp.AddWindow({
        "ID": "MarkShotSettings",
        "WindowTitle": "MarkShot Settings",
        "Geometry": [100, 100, 320, 210],
        "Spacing": 10,
    }, [
        ui.VGroup({"Spacing": 10}, [
            ui.HGroup({"Weight": 0}, [
                ui.Label({"Text": "File Format:", "Weight": 0.4}),
                ui.ComboBox({"ID": "FormatCombo", "Weight": 0.6}),
            ]),
            ui.HGroup({"Weight": 0}, [
                ui.Label({"Text": "Marker Color:", "Weight": 0.4}),
                ui.ComboBox({"ID": "ColorCombo", "Weight": 0.6}),
            ]),
            ui.HGroup({"Weight": 0}, [
                ui.CheckBox({"ID": "BurninCheck", "Text": "Include Data Burn-in", "Checked": True}),
            ]),
            ui.VGap(10),
            ui.HGroup({"Weight": 0}, [
                ui.HGap(0, 1),
                ui.Button({"ID": "OKButton", "Text": "  OK  ", "Weight": 0}),
                ui.Button({"ID": "CancelButton", "Text": "Cancel", "Weight": 0}),
            ]),
        ]),
    ])

    # Get UI elements
    itm = win.GetItems()

    # Populate combo boxes
    itm["FormatCombo"].AddItems(FORMAT_OPTIONS)
    itm["ColorCombo"].AddItems(COLOR_OPTIONS)

    # Set defaults
    itm["FormatCombo"].CurrentIndex = 0  # PNG
    itm["ColorCombo"].CurrentIndex = 0   # All

    # Event handlers
    def on_ok(ev):
        dialog_result["ok"] = True
        dialog_result["format"] = FORMAT_OPTIONS[itm["FormatCombo"].CurrentIndex]
        dialog_result["color"] = COLOR_OPTIONS[itm["ColorCombo"].CurrentIndex]
        dialog_result["burnin"] = itm["BurninCheck"].Checked
        disp.ExitLoop()

    def on_cancel(ev):
        dialog_result["ok"] = False
        disp.ExitLoop()

    def on_close(ev):
        dialog_result["ok"] = False
        disp.ExitLoop()

    # Connect events
    win.On.OKButton.Clicked = on_ok
    win.On.CancelButton.Clicked = on_cancel
    win.On.MarkShotSettings.Close = on_close

    # Show dialog
    win.Show()
    disp.RunLoop()
    win.Hide()

    # Check result
    if not dialog_result["ok"]:
        print("Operation cancelled by user")
        raise SystemExit()

    selected_format = dialog_result["format"]
    selected_color = dialog_result["color"]
    use_burnin = dialog_result["burnin"]

    print(f"Settings: Format={selected_format}, Color={selected_color}, Burn-in={use_burnin}")

except Exception as e:
    # UIManager not available, use defaults
    print(f"Note: Using default settings (JPEG, All markers, Burn-in ON)")
    print(f"  (UIManager error: {e})")
    selected_format = "JPEG"
    selected_color = "All"
    use_burnin = True  # ON (auto-fallback if not available)

print("-" * 60)


# ============================================================
# Helper Functions
# ============================================================

def frame_to_timecode(frame_offset, start_timecode, fps):
    """Convert frame offset (from timeline start) to timecode"""
    h, m, s, f = map(int, start_timecode.replace(';', ':').split(':'))
    start_seconds = h * 3600 + m * 60 + s + f / fps

    # frame_offset is already relative to timeline start
    seconds_diff = frame_offset / fps

    total_seconds = start_seconds + seconds_diff

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    frames = int(round((total_seconds % 1) * fps))

    if frames >= int(fps):
        frames = 0
        seconds += 1
        if seconds >= 60:
            seconds = 0
            minutes += 1
            if minutes >= 60:
                minutes = 0
                hours += 1

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:02d}"


def filter_markers_by_color(markers, color_filter):
    """Filter markers by color"""
    if color_filter == "All":
        return markers
    return {
        frame_id: marker
        for frame_id, marker in markers.items()
        if marker.get('color') == color_filter
    }


# ============================================================
# Apply Color Filter
# ============================================================

filtered_markers = filter_markers_by_color(markers, selected_color)

if not filtered_markers:
    print(f"WARNING: No {selected_color} markers found")
    print(f"   Total markers: {marker_count}, but none match color '{selected_color}'")
    raise SystemExit()

filtered_count = len(filtered_markers)
if selected_color != "All":
    print(f"Filtered: {filtered_count} {selected_color} markers (from {marker_count} total)")
else:
    print(f"Processing: {filtered_count} markers")


# ============================================================
# Output Directory Selection
# ============================================================

default_path = os.path.expanduser(f"~/Desktop")
selected_path = fusion.RequestDir(default_path, "Select Output Folder for Stills")

if selected_path:
    output_dir = os.path.normpath(selected_path)
else:
    print("WARNING: No folder selected. Operation cancelled.")
    raise SystemExit("Operation cancelled by user")
print(f"Output: {output_dir}")
print("-" * 60)


# ============================================================
# Export Frames
# ============================================================

file_prefix = f"{project_name}_"
file_ext = FORMAT_MAP[selected_format]
exported_stills = []
timecodes = []
success_count = 0
failed_count = 0

if use_burnin:
    print("Exporting frames with Data Burn-in...")
else:
    print("Grabbing frames to Gallery...")

# First, clear any existing stills in current album
existing_stills = album.GetStills()
if existing_stills:
    album.DeleteStills(existing_stills)
    print(f"  Cleared {len(existing_stills)} existing stills from album")

for i, (frame_id, marker_info) in enumerate(sorted(filtered_markers.items()), 1):
    try:
        # frame_id is the marker position (frame offset from timeline start)
        # Convert directly to timecode using fps and start_tc
        marker_frame = int(frame_id)

        # Parse start timecode
        tc_parts = start_tc.replace(';', ':').split(':')
        start_h, start_m, start_s, start_f = map(int, tc_parts)

        # Calculate total frames from timeline start TC
        start_total_frames = int((start_h * 3600 + start_m * 60 + start_s) * fps + start_f)

        # Add marker frame offset
        total_frames = start_total_frames + marker_frame

        # Convert frame count to timecode (integer math to avoid rounding errors)
        # For 23.976fps, use frame-based calculation
        frames_per_second = int(round(fps))  # 24 for 23.976

        tc_f = total_frames % frames_per_second
        remaining = total_frames // frames_per_second
        tc_s = remaining % 60
        remaining = remaining // 60
        tc_m = remaining % 60
        tc_h = remaining // 60

        timecode = f"{tc_h:02d}:{tc_m:02d}:{tc_s:02d}:{tc_f:02d}"
        tc_label = f"{tc_h:02d}_{tc_m:02d}_{tc_s:02d}_{tc_f:02d}"

        # Move playhead to marker position
        timeline.SetCurrentTimecode(timecode)
        time.sleep(0.3)

        marker_name = marker_info.get('name', '')
        marker_color = marker_info.get('color', 'Unknown')

        if use_burnin:
            # Export directly with Data Burn-in
            base_name = f"{file_prefix}{tc_label}"
            file_path = os.path.join(output_dir, f"{base_name}.{file_ext}")
            # If file exists, add suffix -2, -3, etc.
            if os.path.exists(file_path):
                counter = 2
                while os.path.exists(os.path.join(output_dir, f"{base_name}-{counter}.{file_ext}")):
                    counter += 1
                file_path = os.path.join(output_dir, f"{base_name}-{counter}.{file_ext}")
            result = project.ExportCurrentFrameAsStill(file_path)

            if result:
                success_count += 1
            else:
                # Fallback to Gallery method (Free version doesn't support ExportCurrentFrameAsStill)
                if i == 1:
                    print("  Data Burn-in not available, using Gallery method...")
                    use_burnin = False
                still = timeline.GrabStill()
                if still:
                    timecodes.append(tc_label)
                    exported_stills.append(still)
                    success_count += 1
                else:
                    failed_count += 1
        else:
            # Grab frame to Gallery
            still = timeline.GrabStill()
            if still:
                timecodes.append(tc_label)
                exported_stills.append(still)
                success_count += 1
            else:
                failed_count += 1

        if marker_name:
            print(f"[{i}/{filtered_count}] OK: {tc_label} ({marker_color}) - {marker_name}")
        else:
            print(f"[{i}/{filtered_count}] OK: {tc_label} ({marker_color})")

    except Exception as e:
        print(f"[{i}/{filtered_count}] ERROR: Frame {frame_id} - {e}")
        failed_count += 1

print("-" * 60)

# Export all stills at once (non-burnin mode only)
if not use_burnin and exported_stills:
    print(f"Exporting {len(exported_stills)} frames from Gallery...")

    # Get files before export
    existing_files = set(glob.glob(os.path.join(output_dir, f"*.{file_ext}")))

    # Export all at once
    album.ExportStills(exported_stills, output_dir, file_prefix, file_ext)
    time.sleep(1.0)

    # Get new files
    all_files = set(glob.glob(os.path.join(output_dir, f"*.{file_ext}")))
    new_files = sorted(list(all_files - existing_files))

    print(f"  Exported {len(new_files)} files")

    # Find files that match pattern "_1.1.X.jpg" (DaVinci auto-generated)
    # These are the correct files, one per still
    import re
    auto_files = []
    extra_files = []
    for f in new_files:
        basename = os.path.basename(f)
        # Pattern: prefix__1.1.X.ext (double underscore before 1.1.X)
        if re.search(r'__\d+\.\d+\.\d+\.' + file_ext + '$', basename):
            auto_files.append(f)
        elif re.search(r'_\d+\.\d+\.\d+\.' + file_ext + '$', basename):
            # Pattern: prefix_TC_1.1.X.ext (TC files with extra suffix)
            extra_files.append(f)

    print(f"  Auto-generated files: {len(auto_files)}, Extra files: {len(extra_files)}")

    # Delete extra files (the ones with TC + suffix)
    for f in extra_files:
        try:
            os.remove(f)
        except:
            pass

    # Rename auto-generated files to TC filenames
    auto_files_sorted = sorted(auto_files)
    if len(auto_files_sorted) == len(timecodes):
        for src_file, tc_label in zip(auto_files_sorted, timecodes):
            base_name = f"{file_prefix}{tc_label}"
            dst_file = os.path.join(output_dir, f"{base_name}.{file_ext}")
            # If file exists, add suffix -2, -3, etc.
            if os.path.exists(dst_file):
                counter = 2
                while os.path.exists(os.path.join(output_dir, f"{base_name}-{counter}.{file_ext}")):
                    counter += 1
                dst_file = os.path.join(output_dir, f"{base_name}-{counter}.{file_ext}")
            try:
                os.rename(src_file, dst_file)
                print(f"  Renamed: {os.path.basename(src_file)} -> {os.path.basename(dst_file)}")
            except Exception as e:
                print(f"  Rename error: {e}")
    else:
        print(f"  Warning: File count mismatch (auto files: {len(auto_files_sorted)}, expected: {len(timecodes)})")

    # Cleanup gallery
    album.DeleteStills(exported_stills)

# Cleanup .drx files
drx_files = glob.glob(os.path.join(output_dir, "*.drx"))
for drx_file in drx_files:
    try:
        os.remove(drx_file)
    except:
        pass

# ============================================================
# Complete
# ============================================================

print("=" * 60)
print("COMPLETE!")
print(f"Format: {selected_format}")
print(f"Color Filter: {selected_color}")
print(f"Data Burn-in: {'ON' if use_burnin else 'OFF'}")
print(f"Success: {success_count} frames")
print(f"Failed: {failed_count} frames")
print(f"Output: {output_dir}")
print("=" * 60)

# Open output folder
print("Opening output folder...")
try:
    if platform.system() == "Darwin":
        subprocess.run(["open", output_dir])
    elif platform.system() == "Windows":
        subprocess.run(["explorer", output_dir])
    else:
        subprocess.run(["xdg-open", output_dir])
except Exception as e:
    print(f"  Could not open folder: {e}")
