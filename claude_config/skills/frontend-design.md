---
name: frontend-design
description: 大胆で独特なフロントエンドデザインを生成。AIっぽい無難なデザインを避け、本番品質のUIを作成。
---

# Frontend Design Skill

## 目的

ジェネリックな「AI生成デザイン」を避け、独特で本番品質のフロントエンドを生成する。

## 適用時の原則

### Typography（タイポグラフィ）
- **禁止**: Inter, Roboto, Arial, system fonts
- **推奨**: 文脈に合った独特なフォント
  - Code系: JetBrains Mono, Fira Code, Space Grotesk
  - Editorial系: Playfair Display, Crimson Pro
  - Startup系: Clash Display, Satoshi, Cabinet Grotesk

### Color & Theme（配色）
- 一貫したテーマにコミット
- CSS変数で統一感を出す
- 支配的な色 + 鋭いアクセント（均等配分より効果的）
- **禁止**: 白背景に紫グラデーション（AIっぽい）

### Motion（アニメーション）
- 高インパクトな瞬間に集中
- ページ読み込み時のスタッガードアニメーション
- 散発的なマイクロインタラクションより効果的

### Backgrounds（背景）
- 単色ではなく、雰囲気と深みを作る
- テクスチャ、グラデーション、パターンを活用

### Layout（レイアウト）
- 予測可能なグリッドから脱却
- 非対称、意外性のある空間構成
- 深みと階層感

## 禁止事項

- Overused font families (Inter, Roboto, Arial)
- Clichéd color schemes (purple gradients on white)
- Predictable layouts
- Cookie-cutter design
- Generic "AI-generated" aesthetics

## 使用例

```
「ダッシュボードを作って」
→ 明確な美的方向性を選択（brutalist, retro-futuristic, minimalist等）
→ 独特なフォントペアリング
→ コンテキストに合った配色
→ インパクトのあるアニメーション
```

## 参考

- [Frontend Aesthetics Cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb)
