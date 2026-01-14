# MarkShot 仕様書
## DaVinci Resolve マーカーフレーム自動書き出しツール

**バージョン**: 1.3.2
**対応環境**: DaVinci Resolve 17.4以降（macOS / Windows）
**開発**: One Frame Studio

---

## 概要

MarkShotは、DaVinci Resolveのタイムライン上に配置したマーカーの位置から、フレーム画像を自動で書き出すスクリプトです。編集確認、クライアントレビュー、サムネイル作成などのワークフローを大幅に効率化します。

**v1.3.0で無料版にも対応しました。**

---

## 主な機能

### 1. マーカー位置からの自動フレーム書き出し

タイムライン上のすべてのマーカー位置を自動検出し、各位置のフレームを画像として書き出します。

- **対応マーカー**: タイムラインマーカー
- **書き出し枚数**: マーカー数に応じて自動（制限なし）
- **処理速度**: 1フレームあたり約0.5〜1秒

### 2. ファイル形式選択

用途に応じて出力形式を選択できます。

| 形式 | 特徴 | 推奨用途 |
|------|------|----------|
| **JPEG** | 軽量、高圧縮 | Web、メール送付、プレビュー |
| **PNG** | 可逆圧縮、透過対応 | 高品質保存、合成素材 |
| **TIFF** | 最高品質 | 印刷、アーカイブ |

### 3. マーカー色フィルタリング

特定の色のマーカーのみを書き出し対象にできます。

**対応色**:
- All（すべて）
- Red / Blue / Green / Cyan / Yellow / Pink / Purple / その他

**活用例**:
- 赤マーカー → 要修正カット
- 青マーカー → クライアント確認用
- 緑マーカー → 完成カット

### 4. データ焼き付け対応

DaVinci Resolveで設定したデータ焼き付け（タイムコード、クリップ名など）を画像に焼き込んで書き出せます。

| 設定 | 出力結果 |
|------|----------|
| **ON**（デフォルト） | タイムコード等が画像に焼き込まれる |
| **OFF** | クリーンな画像（焼き込みなし） |

**活用例**:
- ON → 編集確認用、クライアントレビュー用
- OFF → サムネイル作成用、納品用

### 5. タイムコード付きファイル名

書き出されるファイルには、自動的にタイムコードが付与されます。

**ファイル名形式**:
```
[プロジェクト名]_[時_分_秒_フレーム].jpg
```

**例**:
```
MyProject_00_01_23_15.jpg
MyProject_00_02_45_00.jpg
MyProject_00_05_12_08.jpg
```

### 6. 出力先選択

実行時にフォルダ選択ダイアログが表示され、任意の場所に保存できます。

- デフォルト: デスクトップ
- 書き出し完了後、自動でフォルダを開く

---

## 無料版 vs Studio版

| 機能 | Studio版 | 無料版 |
|------|---------|--------|
| スクリプトメニューから実行 | ✅ | ❌ |
| 設定ダイアログ (UIManager) | ✅ | ❌ |
| データ焼き付け | ✅ | ✅ |
| マーカー色フィルタ | ✅ | ❌（デフォルト: All） |
| ファイル形式選択 | ✅ | ❌（デフォルト: JPEG） |
| Gallery経由の書き出し | ✅ | ✅ |
| Fusionコンソールから実行 | ✅ | ✅ |

---

## 操作フロー

### Studio版

```
1. DaVinci Resolveでタイムラインを開く
         ↓
2. 書き出したい位置にマーカーを配置（Mキー）
         ↓
3. Workspace → Scripts → MarkShot を選択
         ↓
4. 設定ダイアログで選択
   - ファイル形式（JPEG/PNG/TIFF）
   - マーカー色（All/特定色）
   - データ焼き付け（ON/OFF）
         ↓
5. 保存先フォルダを選択
         ↓
6. 自動処理開始
         ↓
7. 完了後、フォルダが自動で開く
```

### 無料版

```
1. DaVinci Resolveでタイムラインを開く
         ↓
2. 書き出したい位置にマーカーを配置（Mキー）
         ↓
3. Fusionページを開く
         ↓
4. Workspace → Console を開く
         ↓
5. exec(open('/path/to/MarkShot.py').read()) を実行
         ↓
6. 保存先フォルダを選択
         ↓
7. 自動処理開始（デフォルト設定）
         ↓
8. 完了後、フォルダが自動で開く
```

---

## 設定ダイアログ（Studio版のみ）

```
┌─────────────────────────────────┐
│ MarkShot Settings               │
├─────────────────────────────────┤
│ File Format:    [JPEG ▼]        │
│ Marker Color:   [All ▼]         │
│ [ ] Include Data Burn-in        │
│                                 │
│           [OK] [Cancel]         │
└─────────────────────────────────┘
```

**注意**: v1.3.1よりデータ焼き付けのデフォルトはONに変更されました。

---

## 動作要件

### ソフトウェア
- **DaVinci Resolve**: 17.4以降（無料版/Studio版）

### OS
- **macOS**: 10.15 (Catalina) 以降
- **Windows**: 10 以降

### DaVinci Resolve設定（Studio版のみ）
- Preferences → System → General
- 「外部スクリプトに使用」→「ローカル」に設定

**注意**: 無料版にはこの設定項目は存在しません。

---

## インストール

### Windows
1. `MarkShotInstaller.exe` を実行
2. 「Install」ボタンをクリック
3. 完了

**インストーラーバージョン**: 1.3.2

### macOS
1. DMGファイルをダウンロード
2. `Install MarkShot.app` をダブルクリック
3. 「Install」ボタンをクリック
4. 完了

### 手動インストール
`MarkShot.py` を以下のフォルダにコピー:

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

### 手動
以下のファイルを削除:
- macOS: `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/MarkShot.py`
- Windows: `%APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility\MarkShot.py`

---

## 活用シーン

### 編集確認
- 修正ポイントにマーカーを配置
- データ焼き付けONで書き出し
- タイムコード付きでクライアントに共有

### サムネイル作成
- 見せ場にマーカーを配置
- データ焼き付けOFFで書き出し
- クリーンな画像をYouTube等に使用

### カット表作成
- 全カットの先頭にマーカーを配置
- 一括書き出し後、Excelやスプレッドシートに貼り付け

### カラーグレーディング確認
- Before/Afterポイントにマーカー配置
- 色別フィルタで比較用画像を書き出し（Studio版）

---

## 技術仕様

### Resolve接続方式（v1.3.0）

3段階で接続を試行：

```python
# Method 1: bmd (Studio版、コンソール)
resolve = bmd.scriptapp("Resolve")

# Method 2: app変数 (無料版対応)
resolve = app.GetResolve()

# Method 3: DaVinciResolveScript (外部実行)
resolve = DaVinciResolveScript.scriptapp("Resolve")
```

### 書き出し方式

| 方式 | 使用API | 対応版 |
|------|---------|--------|
| データ焼き付け ON | `project.ExportCurrentFrameAsStill()` | 両方 |
| データ焼き付け OFF | `timeline.GrabStill()` + `album.ExportStills()` | 両方 |

---

## 制限事項

- **タイムラインマーカーのみ対応**（クリップマーカーは非対応）
- **バックグラウンド実行不可**（処理中はDaVinci Resolveを操作できません）
- **解像度**: 現在のタイムライン/ビューア設定に依存
- **無料版**: 設定ダイアログ・色フィルタは使用不可（デフォルト設定で動作）

---

## ライセンス

MIT License

---

## 開発・サポート

**One Frame Studio**
ヒロ

GitHub Issues で不具合報告・機能要望を受け付けています。
