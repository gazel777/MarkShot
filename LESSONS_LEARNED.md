# MarkShot 開発ガイド
## AIが変わっても理解できるための完全ドキュメント

**最終更新**: 2026-01-11
**バージョン**: v1.2.0
**作成者**: ヒロ / One Frame Studio

---

## 📋 プロジェクト概要

**MarkShot** = DaVinci Resolveのタイムライン上のマーカー位置から、タイムコード付きでフレームを自動書き出しするPythonスクリプト

**特徴**:
- マーカー色でフィルタリング可能
- JPEG/PNG/TIFF形式選択
- Data Burn-in対応（タイムコード焼き込み）

---

## 📁 プロジェクト構成（v1.2.0現在）

```
Davinci_MarkShot/
├── MarkShot.py                    # 本体スクリプト
├── VERSION.txt                    # バージョン管理（Single Source of Truth）
├── README.md                      # ユーザー向けドキュメント
├── CHANGELOG.md                   # 変更履歴
├── LESSONS_LEARNED.md             # このファイル（開発ガイド）
├── build_applescript_installer.sh # macOSインストーラービルド
├── installer_macos/               # AppleScriptソース
│   ├── install_markshot.applescript
│   └── uninstall_markshot.applescript
├── dist_light/                    # ビルド成果物
│   ├── Install MarkShot.app
│   ├── Uninstall MarkShot.app
│   └── MarkShot-vX.X.X-macOS.dmg
└── REF/                           # 参考資料
```

### 削除済み（旧PyInstaller方式）
- ~~build_all.py~~
- ~~installer_gui.py~~
- ~~uninstaller_gui.py~~
- ~~requirements.txt~~
- ~~dist/~~ (24MB → 131KB に削減)

---

## 🏗️ ビルド方法

### macOS（AppleScript方式）

```bash
cd "/Volumes/NVME_2TB/AI_app/Davinci _PlugIns/Davinci_MarkShot"
./build_applescript_installer.sh
```

**出力**: `dist_light/MarkShot-v1.2.0-macOS.dmg` (約130KB)

**含まれるもの**:
- `Install MarkShot.app` - インストーラー
- `Uninstall MarkShot.app` - アンインストーラー

### Windows

現時点ではWindows版未対応。必要な場合はPyInstaller方式で作成。

---

## 🔧 開発環境セットアップ

### シンボリックリンク方式（推奨）

ソース編集 → 即座にDaVinci Resolveで反映：

```bash
ln -sf "/Volumes/NVME_2TB/AI_app/Davinci _PlugIns/Davinci_MarkShot/MarkShot.py" \
  "$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/MarkShot.py"
```

### リンク解除（本番テスト時）

```bash
rm "$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/MarkShot.py"
```

---

## ⚠️ 重要な発見と つまづきポイント

### 1. 【最重要】スクリプト実行環境の違い

DaVinci Resolveには**2つの異なる実行環境**がある：

| 環境 | API接続方法 |
|------|-------------|
| Consoleウィンドウ | `bmd.scriptapp("Resolve")` |
| スクリプトメニュー | `DaVinciResolveScript.scriptapp("Resolve")` |

**両方に対応するコード（必須）**:
```python
try:
    resolve = bmd.scriptapp("Resolve")
except NameError:
    try:
        import DaVinciResolveScript
        resolve = DaVinciResolveScript.scriptapp("Resolve")
    except ImportError:
        raise SystemExit("Cannot import DaVinci Resolve API")
```

### 2. 【重要】文字エンコーディング問題

**問題**: 日本語などの非ASCII文字を直接書き込むとエラー

**解決策**: すべての出力メッセージを英語にする

```python
# NG
print("処理中...")

# OK
print("Processing...")
```

### 3. 【重要】環境設定「外部スクリプトに使用」

**症状**: スクリプトメニューから実行しても何も起こらない

**解決策**:
1. DaVinci Resolve → Preferences → System → General
2. 「外部スクリプトに使用」を「ローカル」に変更
3. DaVinci Resolveを再起動

### 4. ExportCurrentFrameAsStill のオブジェクト

**つまづき**: `timeline.ExportCurrentFrameAsStill()` は存在しない

**正解**: `project.ExportCurrentFrameAsStill(filePath)`

Data Burn-inを含んだフレームを直接書き出すにはこのAPIを使用。

### 5. ExportStillsのファイル名問題

`album.ExportStills()` の出力ファイル名はバージョンによって異なる。
固定パターンを想定せず、**書き出し前後のファイル差分**で検出する：

```python
existing_files = set(glob.glob(os.path.join(output_dir, "*.png")))
result = album.ExportStills(exported_stills, output_dir, file_prefix, "png")
time.sleep(0.5)
all_files = set(glob.glob(os.path.join(output_dir, "*.png")))
new_files = sorted(all_files - existing_files)
```

### 6. シンボリックリンクが反映されない

**症状**: コード変更したのに古いバージョンが動く

**原因**: リンクが切れている or 別ファイルがある

**解決策**: リンクを再作成
```bash
ln -sf "ソースパス" "ターゲットパス"
```

### 7. Consoleで Lua エラー

**症状**: `[string "???"]:1: '=' expected near '-'`

**原因**: Py3タブではなくLuaタブが選択されている

**解決策**: Consoleウィンドウ上部の「Py3」タブをクリック

---

## 📂 インストール先パス

| OS | パス |
|----|------|
| macOS | `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/` |
| Windows | `%APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility\` |

---

## 🎯 MarkShot.py 動作フロー

### Data Burn-in ON（v1.2.0 新方式）
```
1. DaVinci Resolve APIに接続
2. マーカー取得・色フィルタ適用
3. 各マーカー位置に移動
4. project.ExportCurrentFrameAsStill(filePath) で直接書き出し
5. 出力フォルダを開く
```

### Data Burn-in OFF（従来方式）
```
1. DaVinci Resolve APIに接続
2. マーカー取得・色フィルタ適用
3. 各マーカー位置に移動
4. timeline.GrabStill() でGalleryにキャプチャ
5. album.ExportStills() で一括書き出し
6. ファイル名をタイムコード付きにリネーム
7. .drxファイル削除、Galleryスチル削除
8. 出力フォルダを開く
```

---

## 🚀 macOSインストーラー技術選定

### v1.2.0での変更

| 項目 | 旧（PyInstaller） | 新（AppleScript） |
|------|-------------------|-------------------|
| サイズ | 24MB | 131KB |
| 依存関係 | Python, Tkinter | なし |
| ビルド | `python3 build_all.py` | `./build_applescript_installer.sh` |

### 選定基準

```
インストーラーが必要？
  ├─ ファイルコピーだけ → AppleScript（推奨）
  ├─ 簡単なGUI → AppleScript
  ├─ 複雑なGUI → Python + PyInstaller または Swift
  └─ システム深部への変更 → pkgインストーラー
```

### AppleScriptインストーラーの作り方

```bash
# 1. AppleScriptをアプリにコンパイル
osacompile -o "Install App.app" install_script.applescript

# 2. リソースを埋め込む
cp target_file.py "Install App.app/Contents/Resources/"

# 3. Ad-hoc署名
codesign --deep --force -s - "Install App.app"

# 4. DMG作成
hdiutil create -volname "AppName" -srcfolder output_dir -format UDZO output.dmg
```

---

## ✅ チェックリスト

### リリース前確認

- [ ] VERSION.txt を更新
- [ ] CHANGELOG.md を更新
- [ ] `./build_applescript_installer.sh` でビルド
- [ ] DMGを開いてインストーラーをテスト
- [ ] DaVinci Resolveでスクリプト動作確認
- [ ] Data Burn-in ON/OFF 両方テスト
- [ ] アンインストーラーをテスト

### コード変更時確認

- [ ] `bmd` と `DaVinciResolveScript` 両方対応しているか
- [ ] すべての出力メッセージが英語か
- [ ] エラーハンドリングがあるか
- [ ] シンボリックリンクが有効か（開発時）

---

## 📞 トラブルシューティング

| 症状 | 解決策 |
|------|--------|
| スクリプトが表示されない | DaVinci Resolve再起動、ファイルパス確認 |
| 何も起こらない | 環境設定「ローカル」確認、Py3タブ選択 |
| 「開発元を確認できません」 | システム設定 → セキュリティ → 「開く」 |
| UnicodeEncodeError | すべての出力を英語に変更 |
| 古いバージョンが動く | シンボリックリンク再作成 |

---

## 📚 変更履歴サマリー

| バージョン | 主な変更 |
|------------|----------|
| v1.2.0 | Data Burn-in対応、AppleScriptインストーラー、サブフォルダ廃止 |
| v1.1.0 | ファイル形式選択、マーカー色フィルタ、設定ダイアログ |
| v1.0.2 | Ad-hoc署名追加、VERSION.txt導入 |
| v1.0.1 | ExportStillsファイル名問題修正 |
| v1.0.0 | 初回リリース |

詳細は CHANGELOG.md を参照。
