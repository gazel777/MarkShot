#!/bin/bash
# update_version.sh - バージョン番号を一括更新するスクリプト
# 使用方法: ./update_version.sh 1.3.2

set -e

if [ -z "$1" ]; then
    echo "Usage: ./update_version.sh <version>"
    echo "Example: ./update_version.sh 1.3.2"
    exit 1
fi

NEW_VERSION="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=========================================="
echo "Updating version to: $NEW_VERSION"
echo "=========================================="

# 1. VERSION.txt (Single Source of Truth)
echo "$NEW_VERSION" > "$SCRIPT_DIR/VERSION.txt"
echo "✓ VERSION.txt"

# 2. MarkShot.py - コメント行
sed -i '' "s/# v[0-9]\+\.[0-9]\+\.[0-9]\+ -/# v$NEW_VERSION -/" "$SCRIPT_DIR/MarkShot.py"
echo "✓ MarkShot.py (comment)"

# 3. MarkShot.py - print文
sed -i '' "s/Marker Frame Export Tool v[0-9]\+\.[0-9]\+\.[0-9]\+/Marker Frame Export Tool v$NEW_VERSION/" "$SCRIPT_DIR/MarkShot.py"
echo "✓ MarkShot.py (print)"

# 4. README.md
sed -i '' "s/\*\*バージョン\*\*: [0-9]\+\.[0-9]\+\.[0-9]\+/**バージョン**: $NEW_VERSION/" "$SCRIPT_DIR/README.md"
sed -i '' "s/MarkShot-v[0-9]\+\.[0-9]\+\.[0-9]\+/MarkShot-v$NEW_VERSION/g" "$SCRIPT_DIR/README.md"
sed -i '' "s/\*\*インストーラーバージョン\*\*: [0-9]\+\.[0-9]\+\.[0-9]\+/**インストーラーバージョン**: $NEW_VERSION/" "$SCRIPT_DIR/README.md"
echo "✓ README.md"

# 5. SPEC.md
sed -i '' "s/\*\*バージョン\*\*: [0-9]\+\.[0-9]\+\.[0-9]\+/**バージョン**: $NEW_VERSION/" "$SCRIPT_DIR/SPEC.md"
sed -i '' "s/\*\*インストーラーバージョン\*\*: [0-9]\+\.[0-9]\+\.[0-9]\+/**インストーラーバージョン**: $NEW_VERSION/" "$SCRIPT_DIR/SPEC.md"
echo "✓ SPEC.md"

echo ""
echo "=========================================="
echo "Version update complete!"
echo "=========================================="
echo ""
echo "次のステップ:"
echo "1. CHANGELOG.md に変更内容を追記"
echo "2. git add -A && git commit -m \"v$NEW_VERSION\""
echo "3. ./build_applescript_installer.sh でインストーラーをビルド"
echo ""
echo "確認コマンド:"
echo "  grep -r \"$NEW_VERSION\" *.md *.txt MarkShot.py | head -20"
