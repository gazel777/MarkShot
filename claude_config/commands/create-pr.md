現在のブランチの変更内容からPull Requestを作成する。

## 手順

1. `git status` と `git diff` で現在の変更を確認
2. `git log --oneline -10` で最近のコミットを確認
3. 変更内容を分析し、PRのタイトルと説明を作成
4. 未コミットの変更があれば、適切なメッセージでコミット
5. `git push -u origin $(git branch --show-current)` でプッシュ
6. 以下の形式でPRを作成:

```bash
gh pr create --title "PRタイトル" --body "## 概要
変更の概要を記述

## 変更内容
- 変更点1
- 変更点2

## テスト
- [ ] ユニットテスト
- [ ] 動作確認"
```

## 注意事項

- PRタイトルは変更内容を端的に表現
- 説明には「なぜ」この変更が必要かを含める
- 関連するIssueがあれば `Closes #番号` で紐付け
