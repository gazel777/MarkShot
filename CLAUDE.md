# MarkShot プロジェクトルール

## ユーザー指示の解釈ルール

| 指示 | 意味 | 実行内容 |
|------|------|----------|
| **保存** | ローカルgitに保存 | `git add . && git commit` |
| **GitHub** | GitHubにアップ | MarkShot_GitHubにコピー → `git commit` → `git push` |
| **最新版とって** | Macの変更を取得 | `cd MarkShot_GitHub && git pull` → MarkShotにコピー |

**重要**: 「GitHub」と言われるまでpushしない。ローカル作業中は勝手にGitHubにアップしないこと。

---

## Mac/Windows 間の同期ルール

### GitHubリポジトリ

**URL**: https://github.com/gazel777/MarkShot.git

### 同期方法

Mac/Windows間のファイル同期は**必ずGitHub経由**で行う。`REF_to...`フォルダでの手動やり取りは禁止。

**Windows側での手順:**
```bash
# 1. GitHubをclone（初回のみ）
cd "c:/AI-Tools"
git clone https://github.com/gazel777/MarkShot.git MarkShot_GitHub

# 2. Macからの変更を取得
cd "c:/AI-Tools/MarkShot_GitHub"
git pull

# 3. Windows側の変更をpush
git add .
git commit -m "変更内容"
git push
```

### ファイル構成

```
MarkShot_GitHub/
├── MarkShot.py              # メインスクリプト（共通）
├── VERSION.txt              # バージョン（共通）
├── README.md, SPEC.md, CHANGELOG.md  # ドキュメント（共通）
├── installer_macos/         # Mac用インストーラー
└── installer_windows/       # Windows用インストーラー
```

---

## 開発テスト時のルール

### MarkShot.py の更新テスト

MarkShot.py を更新した後のテストでは、**インストーラーをビルドせず**、直接DaVinciのスクリプトフォルダにコピーする:

```bash
cp "c:/AI-Tools/MarkShot/MarkShot.py" "$APPDATA/Blackmagic Design/DaVinci Resolve/Support/Fusion/Scripts/Utility/MarkShot.py"
```

### インストーラービルドが必要なタイミング

- リリース時のみ
- ユーザーが明示的に要求した時

### インストーラーのファイル名規則

**必ずバージョン番号を含める:**
- Windows: `MarkShotInstaller_v1.3.3.exe`, `MarkShotUninstaller_v1.3.3.exe`
- macOS: `MarkShotInstaller_v1.3.3.dmg` など

バージョンなしの名前（`MarkShotInstaller.exe`）は禁止。

## バージョン更新時の変更箇所

1. `VERSION.txt` - Single Source of Truth
2. `MarkShot.py` コメント行 (4行目)
3. `MarkShot.py` print文 (13行目)
4. `README.md` バージョン表示
5. `SPEC.md` バージョン表示
6. `CHANGELOG.md` 新エントリ追加
7. `installer_gui.py` VERSION変数
8. `uninstaller_gui.py` VERSION変数
9. `version_info_installer.txt` filevers/prodvers
10. `version_info_uninstaller.txt` filevers/prodvers
