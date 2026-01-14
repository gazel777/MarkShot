# DaVinci Resolve マーカー付きフレーム書き出しツール
## 要件定義書 v1.0

---

## 1. プロジェクト概要

### 目的
DaVinci Resolveのタイムライン上でマーカーが付けられた位置のフレームを、タイムコード情報を埋め込んだ静止画として自動書き出しするPythonスクリプトツール

### 背景
- 映像制作のワークフローで、重要なシーンにマーカーを付けてレビューや確認を行うことが多い
- 手動でフレームを書き出す作業は時間がかかり非効率
- タイムコード情報がファイル名に含まれていれば、後からタイムライン上の位置を特定しやすい

### ターゲットユーザー
- 映像編集者、ディレクター、プロデューサー
- DaVinci Resolveを使用するポストプロダクション関係者

---

## 2. 機能要件

### 2.1 コア機能

#### マーカー検出
- タイムライン上の全マーカーを取得
- マーカーのフレーム位置を特定
- オプション: 特定の色のマーカーのみを対象にする

#### フレーム書き出し
- 各マーカー位置のフレームを静止画として書き出し
- 対応フォーマット: PNG, JPG, TIFF, DPX
- デフォルトフォーマット: PNG（ロスレス、透過対応）

#### タイムコード埋め込み
- ファイル名にタイムコードを含める
- 形式: `[プロジェクト名]_[タイムコード]_[連番].png`
- 例: `MyProject_01-23-45-12_001.png`

### 2.2 追加機能

#### バッチ処理
- 複数のマーカーを一括処理
- 進捗状況の表示

#### 書き出し設定
- 書き出し先フォルダの指定
- ファイル名プレフィックスのカスタマイズ
- 画像フォーマットの選択

#### エラーハンドリング
- DaVinci Resolveが起動していない場合のエラー処理
- プロジェクト/タイムラインが開かれていない場合の警告
- マーカーが存在しない場合の通知

---

## 3. 技術仕様

### 3.1 使用API

#### DaVinci Resolve Python API
主要なAPIメソッド:
```python
# プロジェクト・タイムライン取得
resolve = dvr_script.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()

# マーカー取得
markers = timeline.GetMarkers()
# 戻り値: dict {frameId: {"color": "色", "name": "名前", "note": "メモ"}}

# タイムコード操作
start_timecode = timeline.GetStartTimecode()
current_tc = timeline.GetCurrentTimecode()
timeline.SetCurrentTimecode(timecode_string)

# フレーム書き出し
still = timeline.GrabStill()  # GalleryStill オブジェクトを返す

# Gallery操作
gallery = project.GetGallery()
album = gallery.GetCurrentStillAlbum()
stills = album.GetStills()
album.ExportStills([still], folder_path, prefix, format)
```

### 3.2 依存関係

#### 必須
- **DaVinci Resolve Studio** (バージョン 17.4以降推奨)
  - 無料版でもAPI利用可能
  - Studio版推奨（機能制限なし）
- **Python 3.10+** (Resolve 18+の場合)
  - Resolve 16-17: Python 3.6+
  - システムのPythonインストールが必要

#### オプション
- **timecode** ライブラリ (タイムコード変換用)
  ```bash
  pip install timecode
  ```

### 3.3 システム要件

#### macOS
- macOS 10.15 Catalina以降
- 環境変数設定:
  ```bash
  export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
  export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
  export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
  ```

#### Windows
- Windows 10 以降
- 環境変数設定:
  ```cmd
  set RESOLVE_SCRIPT_API=%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting
  set RESOLVE_SCRIPT_LIB=C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll
  set PYTHONPATH=%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\
  ```

---

## 4. アーキテクチャ設計

### 4.1 プログラム構造

```
marker_frame_export/
├── marker_frame_export.py      # メインスクリプト
├── README.md                   # 使用方法
├── requirements.txt            # Python依存関係
└── install_script.sh (Mac)     # インストールスクリプト
    └── install_script.bat (Windows)
```

### 4.2 主要クラス/関数

#### MarkerFrameExporter クラス
```python
class MarkerFrameExporter:
    def __init__(self):
        # Resolve接続初期化
    
    def connect_to_resolve(self) -> bool:
        # DaVinci Resolveに接続
    
    def get_markers(self) -> dict:
        # タイムライン上のマーカーを取得
    
    def frame_to_timecode(self, frame: int) -> str:
        # フレーム番号をタイムコードに変換
    
    def export_frame_at_marker(self, frame_id: int, marker_info: dict) -> bool:
        # 指定マーカー位置のフレームを書き出し
    
    def export_all_markers(self, output_dir: str, 
                          file_prefix: str = "",
                          image_format: str = "png",
                          marker_color_filter: str = None) -> int:
        # 全マーカー位置のフレームを書き出し
        # 戻り値: 書き出したフレーム数
```

### 4.3 ワークフロー

```
1. DaVinci Resolveへの接続確認
   ↓
2. 現在のプロジェクト/タイムライン取得
   ↓
3. タイムラインからマーカー情報を取得
   ↓
4. (オプション) マーカーを色でフィルタリング
   ↓
5. 各マーカー位置に対して:
   a. タイムコードを計算
   b. プレイヘッドを移動
   c. GrabStill()で静止画を取得
   d. タイムコード付きファイル名で書き出し
   ↓
6. 完了レポート表示
```

---

## 5. インストール方法

### 5.1 シンプルインストール（推奨）

#### macOS
```bash
# 1. スクリプトをダウンロード
git clone [repository-url]
cd marker_frame_export

# 2. インストールスクリプトを実行
chmod +x install_script.sh
./install_script.sh

# 3. DaVinci Resolve のスクリプトフォルダにコピー
# 自動的に以下にコピーされます:
# /Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/
```

#### Windows
```cmd
REM 1. スクリプトをダウンロード
git clone [repository-url]
cd marker_frame_export

REM 2. インストールスクリプトを実行
install_script.bat

REM 3. DaVinci Resolve のスクリプトフォルダにコピー
REM 自動的に以下にコピーされます:
REM %APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility\
```

### 5.2 手動インストール

1. Python 3.10+をインストール
2. 必要なライブラリをインストール:
   ```bash
   pip install timecode
   ```
3. 環境変数を設定（前述の設定を参照）
4. スクリプトをResolveのUtilityスクリプトフォルダに配置

---

## 6. 使用方法

### 6.1 基本的な使用方法

#### DaVinci Resolve内から実行
1. DaVinci Resolveを起動
2. プロジェクトとタイムラインを開く
3. タイムライン上にマーカーを配置
4. メニュー: `Workspace` → `Scripts` → `Utility` → `Marker Frame Export`
5. 書き出し設定ダイアログで設定
6. 実行

#### コマンドラインから実行
```bash
# macOS/Linux
python3 marker_frame_export.py --output ~/Desktop/frames --format png

# Windows
python marker_frame_export.py --output C:\Users\YourName\Desktop\frames --format png
```

### 6.2 コマンドラインオプション

```bash
marker_frame_export.py [options]

Options:
  -o, --output PATH        出力先ディレクトリ (デフォルト: ~/Desktop/marker_frames)
  -f, --format FORMAT      画像フォーマット png|jpg|tiff|dpx (デフォルト: png)
  -p, --prefix PREFIX      ファイル名プレフィックス (デフォルト: プロジェクト名)
  -c, --color COLOR        フィルタリングするマーカー色 (オプション)
  -q, --quality QUALITY    JPEG品質 1-100 (デフォルト: 95)
  --no-timecode           ファイル名にタイムコードを含めない
  -h, --help              ヘルプを表示
```

### 6.3 使用例

```bash
# 全マーカーをPNGで書き出し
python marker_frame_export.py

# 特定のフォルダに書き出し
python marker_frame_export.py -o /path/to/output

# 青色マーカーのみをJPEGで書き出し
python marker_frame_export.py -c Blue -f jpg

# カスタムプレフィックス付き
python marker_frame_export.py -p "Scene01"
```

---

## 7. 出力ファイル仕様

### 7.1 ファイル命名規則

```
[prefix]_[timecode]_[number].[format]

例:
MyProject_01-23-45-12_001.png
MyProject_01-23-47-08_002.png
Scene01_00-05-30-00_001.jpg
```

### 7.2 タイムコードフォーマット

- **形式**: HH-MM-SS-FF (時-分-秒-フレーム)
- **区切り文字**: ハイフン（ファイル名に使用可能）
- **例**: 
  - 01-23-45-12 (1時間23分45秒12フレーム)
  - 00-00-05-00 (5秒0フレーム)

### 7.3 画像品質設定

- **PNG**: ロスレス圧縮、透過サポート
- **JPG**: 品質設定可能（デフォルト95）
- **TIFF**: ロスレス、プロ向け
- **DPX**: シネマグレード、VFXワークフロー

---

## 8. エラーハンドリング

### 8.1 エラーケースと対応

| エラー状況 | 検出方法 | 対応 |
|---------|--------|------|
| Resolveが起動していない | API接続失敗 | 「DaVinci Resolveを起動してください」と表示 |
| プロジェクトが開かれていない | GetCurrentProject() が None | 「プロジェクトを開いてください」と表示 |
| タイムラインが開かれていない | GetCurrentTimeline() が None | 「タイムラインを開いてください」と表示 |
| マーカーが存在しない | GetMarkers() が空 | 「マーカーが見つかりません」と表示 |
| 書き出し先が存在しない | os.path.exists() | ディレクトリを自動作成 |
| 書き出し権限がない | 書き込みテスト | 権限エラーを表示 |
| タイムコード変換失敗 | 例外キャッチ | デフォルト値を使用、警告表示 |

### 8.2 ロギング

```python
# ログレベル
- INFO: 正常な処理フロー
- WARNING: 潜在的な問題
- ERROR: 処理失敗
- DEBUG: 詳細なデバッグ情報

# ログ出力先
- コンソール（標準出力）
- オプション: ログファイル (marker_export.log)
```

---

## 9. パフォーマンス仕様

### 9.1 処理速度

- **マーカー検出**: < 1秒
- **1フレーム書き出し**: 2-5秒（解像度とフォーマットに依存）
- **100マーカー処理**: 約3-8分

### 9.2 リソース使用

- **メモリ**: 50-200MB
- **CPU**: 書き出し中に集中的に使用
- **ディスク**: 書き出し画像サイズに依存
  - 1080p PNG: 約2-5MB/フレーム
  - 4K PNG: 約8-15MB/フレーム

---

## 10. テスト計画

### 10.1 単体テスト

- [ ] Resolve接続テスト
- [ ] マーカー取得テスト
- [ ] タイムコード変換テスト
- [ ] フレーム書き出しテスト
- [ ] ファイル命名テスト

### 10.2 統合テスト

- [ ] 全マーカー書き出しフロー
- [ ] 色フィルタリング機能
- [ ] 異なる画像フォーマット
- [ ] エラーハンドリング

### 10.3 環境テスト

- [ ] macOS (Big Sur, Monterey, Ventura)
- [ ] Windows (10, 11)
- [ ] DaVinci Resolve (無料版, Studio版)
- [ ] 異なる解像度プロジェクト

---

## 11. 制限事項

### 11.1 API制限

- タイムラインアイテム単位のマーカーは非対応（タイムラインマーカーのみ）
- カスタムメタデータの自動埋め込みは非対応
- バックグラウンド実行不可（Resolveが起動している必要がある）

### 11.2 既知の問題

- Resolveのレンダーキャッシュ設定に依存する場合がある
- 非常に長いタイムライン（10時間以上）では処理が遅くなる可能性
- ネットワークドライブへの書き出しは推奨されない

---

## 12. 将来の拡張機能

### Phase 2 候補機能

- [ ] GUIインターフェース（Tkinter/PyQt）
- [ ] マーカーメモをメタデータとして埋め込み
- [ ] Excelレポート生成（マーカー一覧）
- [ ] マーカー位置の動画クリップ書き出し（前後5秒など）
- [ ] カスタムタイムコードフォーマット
- [ ] バッチプロジェクト処理

### Phase 3 候補機能

- [ ] AIによる自動マーカー配置提案
- [ ] フレーム比較機能
- [ ] クラウドストレージ連携
- [ ] Frame.io統合

---

## 13. ドキュメント

### 13.1 提供ドキュメント

1. **README.md**: 基本的な使い方とインストール方法
2. **INSTALL.md**: 詳細なインストールガイド
3. **API_REFERENCE.md**: 内部API仕様書
4. **TROUBLESHOOTING.md**: トラブルシューティングガイド
5. **CHANGELOG.md**: バージョン履歴

### 13.2 コード内ドキュメント

- 全関数にDocstring
- 複雑なロジックにはインラインコメント
- 型ヒント（Type Hints）を使用

---

## 14. ライセンス

- **ライセンス**: MIT License
- **オープンソース**: GitHub公開
- **商用利用**: 可能

---

## 15. サポート

### 15.1 イシュートラッキング

- GitHub Issues でバグ報告・機能リクエスト

### 15.2 コミュニティ

- GitHub Discussions でQ&A
- BMD Forum での情報共有

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0 | 2025-12-10 | 初版作成 |

---

**作成者**: ヒロ / One Frame Studio  
**最終更新**: 2025年12月10日
