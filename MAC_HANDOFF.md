# MarkShot Mac版 引き継ぎドキュメント

**バージョン**: 1.3.2
**日付**: 2026-01-14

---

## 概要

Windows版でDaVinci Resolve無料版への対応を完了しました（v1.3.2）。
Mac版でも同様のインストーラー作成が必要です。

---

## Mac側AIに送るメッセージ

以下をコピーしてMac側のClaudeに送ってください：

---

MarkShot（DaVinci Resolve用マーカーフレーム書き出しツール）のMac版インストーラーを作成してほしい。

Windows版でv1.3.2として無料版対応を完了。主な変更点：
1. app.GetResolve()による無料版接続対応
2. データ焼き付けデフォルトON
3. タイムコード計算を整数演算のみに修正（23.976fps等での精度向上）
4. Gallery処理改善（実行前クリア、ファイル検出改善）

**重要: v1.3.2の変更点**
- TC計算を整数演算のみで行うように修正（丸め誤差対策）
- データ焼き付けはStudio版/無料版どちらでも動作

添付のMarkShot.pyを使って：
1. Mac用インストーラー（.app / .dmg）を作成
2. 必要ならテスト

無料版では：
- スクリプトメニューから実行不可
- Fusionコンソールからexec()で実行
- UIManagerが使えない（設定ダイアログなし）

---

## 渡すファイル

### 必須
```
MarkShot.py          # 最新版v1.3.2（Free版対応済み）
```

### 参考（任意）
```
VERSION.txt          # バージョン情報
CHANGELOG.md         # 変更履歴
README.md            # README
SPEC.md              # 仕様書
```

---

## v1.3.2の主な変更点

### TC計算精度向上（v1.3.2）
- タイムコード計算を整数演算のみで行うように修正
- 23.976fps等でも正確なTC計算が可能に
- **テスト済み**: 無料版/Studio版どちらでも正常動作確認済み

### データ焼き付け デフォルトON（v1.3.1）
- デフォルトをONに変更

### Resolve接続方法（v1.3.0）

```python
# 3段階で試行
# Method 1: bmd (Studio版、コンソール)
resolve = bmd.scriptapp("Resolve")

# Method 2: app変数 (無料版対応) ← 重要
resolve = app.GetResolve()

# Method 3: DaVinciResolveScript (外部実行)
resolve = DaVinciResolveScript.scriptapp("Resolve")
```

---

## 無料版の機能対応表

| 機能 | Studio版 | 無料版 |
|------|---------|--------|
| スクリプトメニュー | ✅ | ❌ |
| UIManager | ✅ | ❌ |
| データ焼き付け | ✅ | ✅ |
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
Windows: %APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\MarkShot.py
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
├── MarkShotInstaller_v1.3.2.exe    # インストーラー
└── MarkShotUninstaller_v1.3.2.exe  # アンインストーラー
```

インストーラーバージョン: 1.3.2
