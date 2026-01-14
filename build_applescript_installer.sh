#!/bin/bash
# Build lightweight AppleScript installer for MarkShot

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VERSION=$(cat "$SCRIPT_DIR/VERSION.txt" | tr -d '\n')
OUTPUT_DIR="$SCRIPT_DIR/dist_light"
DMG_NAME="MarkShot-v${VERSION}-macOS"

echo "========================================"
echo "Building MarkShot Lightweight Installer"
echo "Version: $VERSION"
echo "========================================"

# Clean previous build
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Build Installer
echo "Compiling Installer..."
osacompile -o "$OUTPUT_DIR/Install MarkShot.app" "$SCRIPT_DIR/installer_macos/install_markshot.applescript"
cp "$SCRIPT_DIR/MarkShot.py" "$OUTPUT_DIR/Install MarkShot.app/Contents/Resources/"
codesign --deep --force -s - "$OUTPUT_DIR/Install MarkShot.app"

# Build Uninstaller
echo "Compiling Uninstaller..."
osacompile -o "$OUTPUT_DIR/Uninstall MarkShot.app" "$SCRIPT_DIR/installer_macos/uninstall_markshot.applescript"
codesign --deep --force -s - "$OUTPUT_DIR/Uninstall MarkShot.app"

# Create DMG
echo "Creating DMG..."
hdiutil create -volname "$DMG_NAME" -srcfolder "$OUTPUT_DIR" -ov -format UDZO "$OUTPUT_DIR/$DMG_NAME.dmg"

# Show results
echo ""
echo "========================================"
echo "BUILD COMPLETE!"
echo "========================================"
echo ""
echo "Output:"
ls -lh "$OUTPUT_DIR/"
echo ""
echo "DMG: $OUTPUT_DIR/$DMG_NAME.dmg"
echo ""

# Get sizes
DMG_SIZE=$(ls -lh "$OUTPUT_DIR/$DMG_NAME.dmg" | awk '{print $5}')
echo "DMG Size: $DMG_SIZE"
