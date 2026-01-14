# MarkShot Mac版 引き継ぎドキュメント

**バージョン**: 1.3.0
**日付**: 2026-01-12

---

## 概要

Windows版でDaVinci Resolve無料版への対応を完了しました（v1.3.0）。
Mac版でも同様のインストーラー作成が必要です。

---

## Mac側AIに送るメッセージ

以下をコピーしてMac側のClaudeに送ってください：

---

MarkShot（DaVinci Resolve用マーカーフレーム書き出しツール）のMac版インストーラーを作成してほしい。

Windows版でv1.3.0として無料版対応を完了。主な変更点：
1. app.GetResolve()による無料版接続対応
2. Data Burn-inデフォルトOFF（無料版では使えない）
3. タイムコード計算修正（frame_idは既に相対位置）
4. Gallery処理改善（実行前クリア、ファイル検出改善）

添付のMarkShot.pyを使って：
1. Mac用インストーラー（.app / .dmg）を作成
2. 必要ならテスト

無料版では：
- スクリプトメニューから実行不可
- Fusionコンソールからexec()で実行
- UIManagerが使えない（設定ダイアログなし）
- ExportCurrentFrameAsStillが使えない

---

## 渡すファイル

### 必須
```
MarkShot.py          # 最新版v1.3.0（Free版対応済み）
```

### 参考（任意）
```
VERSION.txt          # バージョン情報
CHANGELOG.md         # 変更履歴
README.md            # README
SPEC.md              # 仕様書
```

---

## v1.3.0の主な変更点

### 1. Resolve接続方法の追加

```python
# 3段階で試行
# Method 1: bmd (Studio版、コンソール)
resolve = bmd.scriptapp("Resolve")

# Method 2: app変数 (無料版対応) ← 重要
resolve = app.GetResolve()

# Method 3: DaVinciResolveScript (外部実行)
resolve = DaVinciResolveScript.scriptapp("Resolve")
```

### 2. デフォルト設定の変更
- Data Burn-in: ON → **OFF**
- 理由: 無料版では`ExportCurrentFrameAsStill`が使えない

### 3. タイムコード計算の修正
- `frame_id`は既にタイムライン開始からの相対位置
- `start_frame`を引く処理を削除

### 4. Gallery処理の改善
- 実行前にGalleryをクリア
- ExportStills後のファイル検出・リネーム処理を正規表現で改善

---

## 無料版の制限事項

| 機能 | Studio版 | 無料版 |
|------|---------|--------|
| スクリプトメニュー | ✅ | ❌ |
| UIManager | ✅ | ❌ |
| ExportCurrentFrameAsStill | ✅ | ❌ |
| app.GetResolve() | ✅ | ✅ |
| timeline.GrabStill() | ✅ | ✅ |
| album.ExportStills() | ✅ | ✅ |

---

## 無料版での実行方法

1. DaVinci Resolveを起動
2. Fusionページを開く
3. `Workspace` → `Console` を開く
4. 以下を入力して実行：

```python
exec(open('/Users/[ユーザー名]/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/MarkShot.py').read())
```

---

## インストール先

```
Mac:     ~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/MarkShot.py
Windows: %APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility\MarkShot.py
```

---

## Mac版インストーラーの作成方法（参考）

Windows版ではPyInstaller + tkinterを使用。
Mac版では以下の選択肢がある：

### 方法1: AppleScript（推奨、軽量）
- サイズが小さい（約130KB）
- 署名なしでも動作可能

### 方法2: PyInstaller
- Windows版と同じ方式
- サイズが大きい（約24MB）

---

## Windows版の成果物

```
dist\
├── MarkShotInstaller.exe    # インストーラー
└── MarkShotUninstaller.exe  # アンインストーラー
```

インストーラーバージョン: 1.3.0
