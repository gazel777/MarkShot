---
name: pdf-processing
description: PDFからテキスト・テーブル抽出、フォーム入力、ドキュメント結合。縦書きライターのPDF処理に使用。
---

# PDF Processing

## Quick start

Extract text with pdfplumber:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## 縦書きPDF対応

縦書きPDFの場合、文字順序が崩れることがある。対策:

```python
# PyMuPDF (fitz) を使用
import fitz

doc = fitz.open("tategaki.pdf")
for page in doc:
    text = page.get_text("text")
```

## テーブル抽出

```python
with pdfplumber.open("file.pdf") as pdf:
    table = pdf.pages[0].extract_table()
```

## PDF結合

```python
from PyPDF2 import PdfMerger

merger = PdfMerger()
merger.append("file1.pdf")
merger.append("file2.pdf")
merger.write("merged.pdf")
merger.close()
```

## 必要なライブラリ

```bash
pip install pdfplumber PyMuPDF PyPDF2
```
