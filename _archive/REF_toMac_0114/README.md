# MarkShot - DaVinci Resolve Marker Frame Export

DaVinci Resolveのタイムライン上のマーカー位置から、フレームを自動書き出しするスクリプトです。

**バージョン**: 1.3.2

## 機能

- タイムライン上の**すべてのマーカー**を自動検出
- 各マーカー位置のフレームを**JPEG/PNG/TIFF**として書き出し
- ファイル名に**タイムコード**を自動付与
- **マーカー色**でフィルタリング可能
- **Data Burn-in対応** - DaVinciで設定したタイムコード等を画像に焼き込み可能
- **DaVinci Resolve無料版対応** (v1.3.0〜)

## 必要要件

- **DaVinci Resolve 17.4以降** (無料版/Studio版)
- **macOS 10.15以降** または **Windows 10以降**

---

## 無料版 vs Studio版

| 機能 | Studio版 | 無料版 |
|------|---------|--------|
| スクリプトメニューから実行 | ✅ | ❌ |
| 設定ダイアログ (UIManager) | ✅ | ❌ |
| Data Burn-in | ✅ | ✅（自動フォールバック） |
| Gallery経由の書き出し | ✅ | ✅ |

**無料版での注意点:**
- 設定ダイアログは表示されません（デフォルト設定で動作）
- Data Burn-inは自動的にGallery方式にフォールバック
- Fusionコンソールから実行する必要があります

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

### Studio版

1. DaVinci Resolveを起動し、プロジェクトとタイムラインを開く
2. タイムライン上にマーカーを追加（ショートカット: `M`）
3. メニューから `Workspace` → `Scripts` → `MarkShot` を選択
4. 設定ダイアログで以下を選択：
   - **File Format**: JPEG / PNG / TIFF
   - **Marker Color**: All / 特定の色
   - **Include Data Burn-in**: タイムコード等を焼き込むかどうか
5. 保存先フォルダを選択
6. 処理完了後、フォルダが自動で開きます

### 無料版

1. DaVinci Resolveを起動し、プロジェクトとタイムラインを開く
2. タイムライン上にマーカーを追加（ショートカット: `M`）
3. **Fusionページ**を開く
4. `Workspace` → `Console` を開く
5. 以下を入力して実行：
   ```python
   exec(open('C:/Users/[ユーザー名]/AppData/Roaming/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/MarkShot.py').read())
   ```
   **macOSの場合:**
   ```python
   exec(open('/Users/[ユーザー名]/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/MarkShot.py').read())
   ```
6. 保存先フォルダを選択
7. 処理完了後、フォルダが自動で開きます

**注意**: 無料版では設定ダイアログが表示されないため、デフォルト設定（JPEG、全マーカー）で動作します。Data Burn-inは自動的にGallery方式にフォールバックします。

---

## Data Burn-inについて

「Include Data Burn-in」をONにすると、DaVinci Resolveで設定したData Burn-in（タイムコード、ファイル名など）が画像に焼き込まれます。

**デフォルト:** ON（無料版では自動的にOFF相当で動作）

**設定方法:**
1. DaVinci Resolveで `Workspace` → `Data Burn-in` を開く
2. 表示したい情報を設定（タイムコード等）
3. MarkShotを実行

**OFFの場合:** クリーンな画像（焼き込みなし）が書き出されます。

**無料版での動作:** Data Burn-inは自動的にGallery方式にフォールバックするため、エラーなく動作します。

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

ヒロ / One Frame Studio
