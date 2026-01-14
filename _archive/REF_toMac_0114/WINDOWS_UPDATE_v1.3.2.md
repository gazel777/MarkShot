# MarkShot v1.3.2 Windows Update Guide

**作成日**: 2026-01-14
**対象バージョン**: v1.3.1 → v1.3.2

---

## 変更概要

### v1.3.2 バグ修正

**問題**: ファイル名のタイムコードがタイムライン上のマーカー位置TCと一致していなかった

**原因**: 浮動小数点演算による丸め誤差（23.976fps等で発生）

**修正内容**: フレーム数からタイムコードへの変換を整数演算のみで行うように変更

---

## 更新されたファイル

| ファイル | 更新内容 |
|----------|----------|
| `MarkShot.py` | TC計算ロジック修正、バージョン番号更新 |
| `VERSION.txt` | 1.3.2 |
| `CHANGELOG.md` | v1.3.2エントリ追加 |
| `README.md` | バージョン番号更新 |
| `SPEC.md` | バージョン番号更新 |

---

## Windows側での作業

### 1. ファイルをコピー

以下のファイルをWindowsプロジェクトにコピー：

```
REF_toMac_0114/
├── MarkShot.py        ← メインスクリプト（必須）
├── VERSION.txt        ← バージョン（必須）
├── CHANGELOG.md       ← 任意
├── README.md          ← 任意
└── SPEC.md            ← 任意
```

### 2. インストーラーをリビルド

```cmd
cd <プロジェクトフォルダ>
python build_installer.py
```

出力：
- `dist/MarkShotInstaller.exe`
- `dist/MarkShotUninstaller.exe`

### 3. 動作確認

1. DaVinci Resolve Studio版を起動
2. タイムラインにマーカーを追加
3. `Workspace` → `Scripts` → `MarkShot` を実行
4. **確認ポイント**:
   - コンソールに `v1.3.2` が表示されること
   - 書き出されたファイル名のTCがタイムライン位置と一致すること

---

## コード変更箇所

### MarkShot.py 341-353行目付近

**変更前（v1.3.1）**: 浮動小数点演算
```python
total_seconds = total_frames / fps
tc_h = int(total_seconds // 3600)
tc_m = int((total_seconds % 3600) // 60)
tc_s = int(total_seconds % 60)
tc_f = int(round((total_seconds - int(total_seconds)) * fps))
```

**変更後（v1.3.2）**: 整数演算のみ
```python
frames_per_second = int(round(fps))  # 24 for 23.976
tc_f = total_frames % frames_per_second
remaining = total_frames // frames_per_second
tc_s = remaining % 60
remaining = remaining // 60
tc_m = remaining % 60
tc_h = remaining // 60
```

---

## テストチェックリスト

- [ ] バージョン表示が `v1.3.2` になっている
- [ ] 23.976fps タイムラインでTC計算が正確
- [ ] 24fps タイムラインでTC計算が正確
- [ ] 29.97fps タイムラインでTC計算が正確
- [ ] Data Burn-in ON で正常に書き出し
- [ ] Data Burn-in OFF で正常に書き出し
- [ ] マーカー色フィルタが動作する
- [ ] インストーラーが正常に動作する
- [ ] アンインストーラーが正常に動作する

---

## 注意事項

### バージョン番号の更新箇所

今後バージョンを上げる際は、以下のすべてを更新すること：

1. `VERSION.txt` - Single Source of Truth
2. `MarkShot.py` コメント行 (4行目)
3. `MarkShot.py` print文 (13行目)
4. `README.md` バージョン表示
5. `SPEC.md` バージョン表示
6. `CHANGELOG.md` 新エントリ追加

**macOSでは `update_version.sh` スクリプトで一括更新可能**

---

## 問題があった場合

macOS側の担当者に連絡：
- 問題の詳細
- 再現手順
- エラーメッセージ（あれば）
