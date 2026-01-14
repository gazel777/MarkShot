# MarkShot 変更履歴

## [v1.3.2] - 2026-01-14

### 🐛 バグ修正

#### タイムコードの修正
- **問題**: ファイル名のタイムコードが、タイムライン上のマーカー位置TCと一致していなかった（浮動小数点演算による丸め誤差）
- **修正**: フレーム数からタイムコードへの変換を**整数演算のみ**で行うように変更
- **変更内容**:
  - `round()` による丸め誤差を排除
  - `total_frames % frames_per_second` で正確なフレーム数を計算
  - 23.976fps等でも正確なTC計算が可能に
- これにより、ファイル名がマーカー位置のタイムラインTCと正確に一致するようになった

---

## [v1.3.1] - 2026-01-12

### 🔧 改善

#### データ焼き付け デフォルトON
- デフォルト設定を**ON**に変更
- Studio版/無料版どちらでも同じ設定で動作

---

## [v1.3.0] - 2026-01-12

### ✨ 新機能

#### DaVinci Resolve 無料版対応
- `app.GetResolve()` による無料版でのAPI接続に対応
- 無料版でもFusionコンソールから実行可能に
- 3段階のResolve接続方式を実装:
  1. `bmd.scriptapp()` - Studio版、コンソール
  2. `app.GetResolve()` - 無料版対応（新規追加）
  3. `DaVinciResolveScript` - 外部実行

### 🔧 改善

#### Gallery処理の改善
- 実行前にGalleryの既存スチルをクリア
- ExportStills後のファイル検出・リネーム処理を正規表現で改善
- 自動生成ファイルと余分なファイルを正確に識別

#### タイムコード計算の修正
- `frame_id`は既にタイムライン開始からの相対位置
- 不要な`start_frame`の減算処理を削除

### 📦 インストーラー

#### Windows インストーラー v1.3.0
- PyInstaller + tkinter によるGUIインストーラー
- `MarkShotInstaller.exe` - インストール
- `MarkShotUninstaller.exe` - アンインストール

### 📝 無料版の機能対応表

| 機能 | Studio版 | 無料版 |
|------|---------|--------|
| スクリプトメニュー | ✅ | ❌ |
| UIManager（設定ダイアログ）| ✅ | ❌ |
| データ焼き付け | ✅ | ✅ |
| app.GetResolve() | ✅ | ✅ |
| timeline.GrabStill() | ✅ | ✅ |
| album.ExportStills() | ✅ | ✅ |

---

## [v1.2.0] - 2026-01-11

### ✨ 新機能

#### データ焼き付け対応
- 設定ダイアログに「Include Data Burn-in」チェックボックスを追加
- DaVinciで設定したデータ焼き付け（タイムコード等）を画像に焼き込んで書き出し可能
- `ExportCurrentFrameAsStill` APIを使用（新方式）
- チェックOFF時は従来のGallery経由の書き出し（クリーンな画像）

### 🔧 改善

#### 保存先の簡素化
- サブフォルダ（MarkShot_XXX）の自動作成を廃止
- 選択したフォルダに直接保存するように変更

#### デフォルト形式変更
- デフォルト出力形式をPNGからJPEGに変更

### 📦 インストーラー刷新

#### AppleScript方式に移行（macOS）
- PyInstaller → AppleScript に変更
- **サイズ: 24MB → 131KB（99.5%削減）**
- DMG形式で配布
- インストーラー/アンインストーラー両方同梱

#### 不要ファイルの削除
- 旧PyInstaller関連ファイルを削除
- ドキュメントを整理・統合

---

## [v1.1.0] - 2026-01-11

### ✨ 新機能

#### ファイル形式選択
- PNG / JPEG / TIFF から出力形式を選択可能に
- 設定ダイアログで選択、ExportStills APIに動的に渡す

#### マーカー色フィルタ
- 特定の色のマーカーのみを書き出し対象にできる
- 対応色: All / Red / Blue / Green / Cyan / Yellow / Pink / Purple
- 「All」選択で従来通り全マーカーを処理

### 🔧 改善

#### 設定ダイアログの追加
- Fusion UIManagerを使用したGUIダイアログ
- ファイル形式とマーカー色を実行前に選択
- UIManager非対応環境ではデフォルト値（PNG, All）で動作

---

## [v1.0.2] - 2026-01-11

### 🔐 セキュリティ改善

#### macOS Ad-hoc署名の追加
- **目的**: Gatekeeper警告の改善（「破損しています」→「開発元を確認できません」）
- **変更内容**: `build_all.py` にAd-hoc署名機能を追加
- ビルド後に自動で `codesign --deep --force -s -` を実行
- Windowsには影響なし（`if system == "Darwin"` で分岐）

### 🔧 開発改善

#### バージョン管理の一元化
- `VERSION.txt` を新規作成（Single Source of Truth）
- `build_all.py` がVERSION.txtからバージョンを読み込み・表示
- `create_release.sh` がVERSION.txtからバージョンを読み込み

#### Windows開発引き継ぎドキュメント
- `WINDOWS_TODO.md` を新規作成
- macOSでの変更内容サマリー
- Windowsで必要な作業リスト
- 注意点・ハマりやすいポイント
- テストチェックリスト

---

## [v1.0.1] - 2025-12-12

### 🐛 バグ修正

#### 画像書き出し時のファイル名問題を修正
- **問題**: `ExportStills`で書き出される画像のファイル名が、想定していた形式（`{prefix}{000001}.png`）と異なっていたため、タイムコード付きへのリネームが機能していなかった
- **修正内容**: 書き出し前後のファイル差分を比較して、新しく作成されたファイルを確実に検出してリネームするように変更
- **修正ファイル**: `MarkShot.py` (166-216行目付近)

```python
# 修正前: ファイル名を想定（動作しない場合があった）
old_name = f"{file_prefix}{i+1:06d}.png"

# 修正後: 実際のファイルを検出
existing_files = set(glob.glob(os.path.join(output_dir, "*.png")))  # 書き出し前
# ... ExportStills実行 ...
all_files = set(glob.glob(os.path.join(output_dir, "*.png")))  # 書き出し後
new_files = sorted(all_files - existing_files)  # 差分 = 新規ファイル
```

### ✨ 新機能

#### Windows用ビルドサポート
- `build_windows.bat` を追加 - ダブルクリックでWindows用インストーラーをビルド
- `WINDOWS_BUILD_README.txt` を追加 - 日本語の手順書

### 🔧 開発改善

#### 開発用シンボリックリンク方式の導入
- 毎回インストーラーでデプロイする代わりに、シンボリックリンクを使用
- ソースファイルを編集するだけで即座にDaVinci Resolveでテスト可能

```bash
# シンボリックリンク作成コマンド（macOS）
ln -sf "/Volumes/NVME_2TB/AI_app/Davinci _PlugIns/Davinci_MarkShot/MarkShot.py" \
  "$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/MarkShot.py"
```

---

## [v1.0.0] - 2025-12-10

### 初回リリース
- 基本的なマーカーフレーム書き出し機能
- タイムコード付きファイル名
- 色フィルタリング機能
- macOS/Windows対応インストーラー/アンインストーラー

