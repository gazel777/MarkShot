# MarkShot - DaVinci Resolve Marker Frame Export

DaVinci Resolveのタイムライン上のマーカー位置から、フレームを自動書き出しするスクリプトです。

**バージョン**: 1.3.3

## 機能

- タイムライン上の**すべてのマーカー**を自動検出
- 各マーカー位置のフレームを**JPEG/PNG/TIFF**として書き出し
- ファイル名に**タイムコード**を自動付与
- **マーカー色**でフィルタリング可能
- **データ焼き付け対応** - DaVinciで設定したデータ焼き付け（タイムコード等）を画像に焼き込み可能
- **DaVinci Resolve無料版対応** (v1.3.0〜)
- **重複ファイル名の自動連番** - 同名ファイルがある場合は `-2`, `-3` を自動付与 (v1.3.3〜)

## 必要要件

- **DaVinci Resolve 17.4以降** (無料版/Studio版)
- **macOS 10.15以降** または **Windows 10以降**

---

## 無料版 vs Studio版

| 機能 | Studio版 | 無料版 |
|------|---------|--------|
| データ焼き付け | ✅ | ✅ |
| 出力形式の選択 (JPEG/PNG/TIFF) | ✅ | ❌（JPEGのみ） |
| マーカー色でフィルタリング | ✅ | ❌（全マーカー） |

**無料版での注意点:**
- 設定ダイアログは表示されません（デフォルト設定で動作）

---

## インストール

### Windows（インストーラー使用）

1. [Releases](../../releases)から `MarkShot-v1.3.2-Windows.zip` をダウンロード
2. ZIPを解凍
3. `MarkShotInstaller.exe` を実行
4. 「Install」ボタンをクリック
5. 完了

**インストーラーバージョン**: 1.3.2

### macOS（インストーラー使用）

1. [Releases](../../releases)から `MarkShot-v1.3.2-macOS.dmg` をダウンロード
2. DMGをダブルクリックしてマウント
3. `Install MarkShot.app` をダブルクリック
4. 「Install」ボタンをクリック
5. 完了

### 手動インストール

`MarkShot.py` を以下のフォルダにコピー：

**Windows:**
```
%APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility\
```

**macOS:**
```
~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/
```

---

## アンインストール

### Windows
- `MarkShotUninstaller.exe` を実行

### macOS
- DMG内の `Uninstall MarkShot.app` を実行

### 手動アンインストール

以下のファイルを削除：

**Windows:**
1. エクスプローラーで以下を開く：
   ```
   %APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility
   ```
2. `MarkShot.py` を削除

**macOS:**
1. Finderで `Shift + Command + G`（フォルダへ移動）
2. 以下を入力：
   ```
   ~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility
   ```
3. `MarkShot.py` を削除

---

## 使用方法

### 初回起動時

初回起動時に「スタジオ版ですか？」の確認ダイアログが表示されます。選択後、**もう一度スクリプトを実行してください**（初回は設定の保存のみで、書き出しは行われません）。

### Studio版

1. DaVinci Resolveを起動し、プロジェクトとタイムラインを開く
2. タイムライン上にマーカーを追加（ショートカット: `M`）
3. メニューから `Workspace` → `Scripts` → `MarkShot` を選択
4. 設定ダイアログで以下を選択：
   - **File Format**: JPEG / PNG / TIFF
   - **Marker Color**: All / 特定の色
   - **Include Data Burn-in**: データ焼き付けを含めるかどうか
5. 保存先フォルダを選択
6. 処理完了後、フォルダが自動で開きます

### 無料版

1. DaVinci Resolveを起動し、プロジェクトとタイムラインを開く
2. タイムライン上にマーカーを追加（ショートカット: `M`）
3. メニューから `Workspace` → `Scripts` → `MarkShot` を選択
4. 保存先フォルダを選択
5. 処理完了後、フォルダが自動で開きます

**初回起動時の注意（無料版のみ）:**
初回起動時に「Are you using Studio version?」の確認ダイアログが表示されます。「No」を選択してください。初回は書き出しが行われますが、静止画が正しくない場合があります。**2回目以降は正常に動作します**ので、もう一度スクリプトを実行してください。

**注意**: 無料版では設定ダイアログが表示されないため、デフォルト設定（JPEG、全マーカー、データ焼き付けON）で動作します。

---

## データ焼き付けについて

「Include Data Burn-in」をONにすると、DaVinci Resolveで設定したデータ焼き付け（タイムコード、ファイル名など）が画像に焼き込まれます。

**デフォルト:** ON

**設定方法:**
1. DaVinci Resolveで `ワークスペース` → `データ焼き付け` を開く
2. 表示したい情報を設定（タイムコード等）
3. MarkShotを実行

**OFFの場合:** クリーンな画像（焼き込みなし）が書き出されます。

---

## 出力ファイル

ファイル名形式：
```
[ProjectName]_[HH_MM_SS_FF].jpg
```

例: `MyMovie_00_01_23_15.jpg`

---

## トラブルシューティング

### スクリプトが表示されない（Studio版）

- DaVinci Resolveを再起動してください
- ファイルが正しい場所にあるか確認してください
- `Preferences` → `System` → `General` → 「外部スクリプトに使用」→「ローカル」に設定

### 「Cannot connect to DaVinci Resolve」エラー

- DaVinci Resolveが起動しているか確認
- Fusionページが開いているか確認（無料版の場合）
- コンソールから正しく実行しているか確認

### 「開発元を確認できません」と表示される（macOS）

1. システム設定 → プライバシーとセキュリティ
2. 「このまま開く」をクリック

### 画像が正しく書き出されない

- タイムラインにマーカーがあるか確認
- プロジェクトとタイムラインが開いているか確認

---

## ライセンス

MIT License

## 作者

Hiro / FrameTools
