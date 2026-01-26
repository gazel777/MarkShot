# グローバル開発ルール

## Git 設定

| 項目 | 値 |
|------|-----|
| **user.name** | hiro |
| **user.email** | hangiyatokyo@gmail.com |

### 確認コマンド

```bash
git config user.name
git config user.email
```

---

## MCP（Model Context Protocol）使用ルール

### 利用可能なMCPサーバー

| MCP | 用途 |
|-----|------|
| **Context7** | ライブラリ/フレームワークの最新ドキュメント取得 |
| **Serena** | コードベース理解・シンボル検索・LSP機能 |
| **Chrome DevTools** | ブラウザデバッグ・パフォーマンス分析 |
| **Playwright** | E2Eテスト・ブラウザ自動操作 |

### 使用方針

1. **Context7**: **必須** - 全プロジェクトで常に使用（最新ドキュメント取得）
2. **その他のMCP**: 小規模プロジェクトは無視OK、必要な場合はClaudeが宣言

### Claudeが宣言するタイミング
- **Serena**: 大規模コードベースでシンボル検索が必要な時
- **Chrome DevTools**: フロントエンドのデバッグ・パフォーマンス問題
- **Playwright**: E2Eテストの作成・実行が必要な時

### 設定ファイル

`~/.claude/.mcp.json` にグローバル設定済み
