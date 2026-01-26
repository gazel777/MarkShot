コードベースのセキュリティチェックを実行する。

対象: $ARGUMENTS（空欄の場合はプロジェクト全体）

## チェック項目

### 1. 機密情報の漏洩チェック
- `.env` ファイルがgit管理されていないか
- APIキー、パスワードのハードコード
- 秘密鍵、認証トークンの露出

```bash
# 機密情報パターンの検索
grep -r "API_KEY\|SECRET\|PASSWORD\|TOKEN" --include="*.ts" --include="*.js" --include="*.json"
```

### 2. OWASP Top 10 ベースのチェック

#### インジェクション
- SQLクエリの文字列連結
- `dangerouslySetInnerHTML` / `v-html` の使用
- `eval()` / `new Function()` の使用

#### アクセス制御
- 認証チェックの欠如
- ユーザーIDベースの権限検証
- IDOR（Insecure Direct Object Reference）

#### セキュリティ設定
- CORS設定
- HTTPSの強制
- セキュリティヘッダー

### 3. 依存関係のチェック

```bash
# npm の場合
npm audit

# pnpm の場合
pnpm audit
```

### 4. BaaS設定のチェック（該当する場合）
- Firebase Security Rules
- Supabase RLS（Row Level Security）

## 出力形式

```
## セキュリティレポート

### 重大な問題 (Critical)
- [ ] 問題の説明と場所

### 高リスク (High)
- [ ] 問題の説明と場所

### 中リスク (Medium)
- [ ] 問題の説明と場所

### 推奨事項
- 改善提案
```

## 注意事項

- 重大な問題は即座に報告
- 修正方法を具体的に提示
- 偽陽性の可能性がある場合は明記
