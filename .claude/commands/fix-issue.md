GitHub Issue #$ARGUMENTS を解決する。

## 手順

1. `gh issue view $ARGUMENTS --comments` でIssue本文とコメントを取得
2. 問題の内容を理解し、実装計画を立てる
3. `git switch -c fix/issue-$ARGUMENTS` で作業ブランチを作成
4. 必要な修正を実装
5. テストを実行して動作確認
6. Linter/Formatterを実行
7. 変更をコミット（コミットメッセージに `Closes #$ARGUMENTS` を含める）
8. `git push -u origin fix/issue-$ARGUMENTS` でプッシュ
9. `gh pr create --fill` でPull Requestを作成

## 注意事項

- 修正範囲は最小限に留める
- 既存のコーディング規約に従う
- テストが通ることを確認してからコミット
