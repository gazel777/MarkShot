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

## ドキュメント編集時のルール

以下のファイルを編集する前に `git pull` で最新を取得すること:
- `README.md`
- `CHANGELOG.md`
- `SPEC.md`
- `VERSION.txt`
- `CLAUDE.md`

編集後は `git push` でGitHubに反映。

---

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

---

## 開発フロー（GitHub Issues/PR）

### バグ修正・機能追加の流れ

```
1. Issue作成（問題や要望を記録）
2. ブランチ作成: git checkout -b fix/issue-番号
3. 修正・実装
4. コミット & プッシュ
5. PR作成: gh pr create
6. CodeRabbitが自動レビュー（日本語）
7. 「マージして」→ mainに反映
8. Issueに経緯をコメント → 自動クローズ（PRに Fixes #番号 を書く）
```

### 進捗管理

- **ドキュメントは増やさない**
- GitHub Issues/PR で全て管理
- 経緯・履歴はIssueのコメントに記録

### CodeRabbit連携

- 設定ファイル: `.coderabbit.yaml`
- 全PRを自動レビュー（日本語）
- 手動レビュー依頼: PRコメントに `@coderabbitai review`

---

## Windowsテスト用インストーラー（友人向け）

### 必要ファイル

| ファイル | 用途 |
|----------|------|
| `MarkShot.py` | 本体スクリプト |
| `install_test.bat` | インストーラー（batファイル） |

### 友人の手順

1. GitHubから `MarkShot.py` をダウンロード（Raw → 右クリック保存）
2. `install_test.bat` も同様にダウンロード
3. **両方を同じフォルダに置く**
4. `install_test.bat` をダブルクリック
5. DaVinci Resolve を起動（または再起動）
6. Workspace → Scripts → Utility → MarkShot

### エラー報告

問題があれば `install_log.txt` を送ってもらう（診断情報が記録されている）

### 注意

- batファイルはMacで作成してOK（テキストファイルなので）
- exeインストーラーはリリース時のみビルド

---

## Windows側 Claude Code 設定

### 概要

Mac側で設定したClaude Codeのグローバル設定（権限、除外ルール、カスタムコマンド等）をWindows側でも使えるようにする。

### セットアップ方法

```bash
# 1. MarkShotリポジトリを同期
cd c:/AI-Tools/MarkShot_GitHub
git pull

# 2. セットアップスクリプトを実行
setup_claude_windows.bat
```

### 含まれる設定

| ファイル/フォルダ | 内容 |
|------------------|------|
| `settings.json` | 権限設定（git, gh, npm等を許可、rm -rf等を禁止） |
| `.claudeignore` | 除外ルール（node_modules, .env, 大きいファイル等） |
| `.mcp.json` | MCP設定（Context7, Serena, Chrome DevTools, Playwright） |
| `CLAUDE.md` | グローバルルール |
| `commands/` | カスタムコマンド（/fix-issue, /create-pr 等） |
| `skills/` | スキル（PDF処理等） |
| `templates/` | CLAUDE.mdテンプレート |
| `docs/` | プロンプトパターン、ワークフロー、セキュリティガイド |

### 利用可能なカスタムコマンド

| コマンド | 用途 |
|----------|------|
| `/fix-issue 番号` | GitHub Issueを修正 |
| `/create-pr` | PRを作成 |
| `/add-feature` | 新機能追加 |
| `/review-code` | コードレビュー |
| `/security-check` | セキュリティ監査 |
| `/init-project` | プロジェクト初期化 |

### 注意

- `setup_claude_windows.bat` は初回のみ実行
- 設定を更新したい場合は再度実行（上書きされる）
- `claude_config/` フォルダに設定ファイルが格納されている
