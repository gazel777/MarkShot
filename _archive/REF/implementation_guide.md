# DaVinci Resolve マーカーフレーム書き出しツール
## 実装ガイド（AI Coding Assistant向け）

---

## プロジェクト概要

**目的**: DaVinci Resolveのタイムライン上のマーカー位置から、タイムコード情報付きでフレームを自動書き出しするPythonスクリプト

**主要機能**:
1. タイムライン上のマーカーを検出
2. 各マーカー位置のフレームを静止画として取得
3. タイムコードをファイル名に埋め込んで保存

---

## 技術スタック

- **言語**: Python 3.10+
- **主要API**: DaVinci Resolve Python API
- **依存ライブラリ**: 
  - `DaVinciResolveScript` (Resolve付属)
  - オプション: `timecode` (pip install timecode)

---

## ファイル構成

```
marker_frame_export/
├── marker_frame_export.py    # メインスクリプト
├── requirements.txt          # 依存関係
├── README.md                # 使用方法
├── install.sh (Mac)         # インストールスクリプト
└── install.bat (Windows)    # インストールスクリプト
```

---

## 実装仕様

### 1. クラス設計

```python
class MarkerFrameExporter:
    """DaVinci Resolveからマーカー位置のフレームを書き出すクラス"""
    
    def __init__(self):
        """初期化"""
        self.resolve = None
        self.project = None
        self.timeline = None
        self.gallery = None
        self.album = None
        
    def connect_to_resolve(self) -> bool:
        """DaVinci Resolveに接続"""
        # DaVinciResolveScript.scriptapp("Resolve")を使用
        # 接続成功時にself.resolveを設定
        
    def get_timeline_info(self) -> dict:
        """タイムライン情報を取得"""
        # 戻り値:
        # {
        #     "name": str,
        #     "start_frame": int,
        #     "start_timecode": str,
        #     "fps": float
        # }
        
    def get_markers(self, color_filter: str = None) -> dict:
        """マーカーを取得（オプションで色フィルタリング）"""
        # timeline.GetMarkers()を使用
        # color_filterが指定されている場合、該当色のマーカーのみ返す
        
    def frame_to_timecode(self, frame: int, start_frame: int, 
                         start_timecode: str, fps: float) -> str:
        """フレーム番号をタイムコードに変換"""
        # "HH:MM:SS:FF" 形式で返す
        
    def export_frame_at_marker(self, frame_id: int, marker_info: dict,
                              output_dir: str, file_prefix: str,
                              image_format: str) -> bool:
        """指定マーカー位置のフレームを書き出し"""
        # 1. SetCurrentTimecode()で位置移動
        # 2. GrabStill()でフレーム取得
        # 3. タイムコードラベルを設定
        
    def export_all_markers(self, output_dir: str, 
                          file_prefix: str = "",
                          image_format: str = "png",
                          color_filter: str = None) -> dict:
        """全マーカーを一括書き出し"""
        # 戻り値: {"success": int, "failed": int, "output_dir": str}
        
    def cleanup_gallery(self, stills: list):
        """Galleryから静止画を削除"""
        # album.DeleteStills(stills)
```

### 2. 主要メソッドの実装

#### connect_to_resolve()

```python
def connect_to_resolve(self) -> bool:
    """
    DaVinci Resolveに接続
    
    Returns:
        bool: 接続成功時True
    """
    try:
        import DaVinciResolveScript as dvr_script
        self.resolve = dvr_script.scriptapp("Resolve")
        
        if not self.resolve:
            print("エラー: DaVinci Resolveが起動していません")
            return False
            
        # プロジェクトとタイムラインを取得
        pm = self.resolve.GetProjectManager()
        self.project = pm.GetCurrentProject()
        
        if not self.project:
            print("エラー: プロジェクトが開かれていません")
            return False
            
        self.timeline = self.project.GetCurrentTimeline()
        
        if not self.timeline:
            print("エラー: タイムラインが開かれていません")
            return False
            
        # Gallery設定
        self.gallery = self.project.GetGallery()
        self.album = self.gallery.GetCurrentStillAlbum()
        
        print(f"接続成功: {self.project.GetName()}")
        return True
        
    except Exception as e:
        print(f"接続エラー: {e}")
        return False
```

#### frame_to_timecode()

```python
def frame_to_timecode(self, frame: int, start_frame: int, 
                     start_timecode: str, fps: float) -> str:
    """
    フレーム番号をタイムコードに変換
    
    Args:
        frame: 対象フレーム番号
        start_frame: タイムライン開始フレーム
        start_timecode: タイムライン開始タイムコード "HH:MM:SS:FF"
        fps: フレームレート
        
    Returns:
        str: タイムコード "HH:MM:SS:FF"
    """
    # start_timecodeを秒に変換
    h, m, s, f = map(int, start_timecode.replace(';', ':').split(':'))
    start_seconds = h * 3600 + m * 60 + s + f / fps
    
    # フレーム差分を秒に変換
    frame_diff = frame - start_frame
    seconds_diff = frame_diff / fps
    
    # 合計秒数
    total_seconds = start_seconds + seconds_diff
    
    # タイムコードに変換
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    frames = int(round((total_seconds % 1) * fps))
    
    # フレームオーバーフロー処理
    if frames >= int(fps):
        frames = 0
        seconds += 1
        if seconds >= 60:
            seconds = 0
            minutes += 1
            if minutes >= 60:
                minutes = 0
                hours += 1
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:02d}"
```

#### export_all_markers()

```python
def export_all_markers(self, output_dir: str, 
                      file_prefix: str = "",
                      image_format: str = "png",
                      color_filter: str = None) -> dict:
    """
    全マーカーを一括書き出し
    
    Args:
        output_dir: 出力ディレクトリ
        file_prefix: ファイル名プレフィックス
        image_format: 画像フォーマット (png, jpg, tiff, dpx)
        color_filter: マーカー色フィルター（Noneで全て）
        
    Returns:
        dict: {"success": 成功数, "failed": 失敗数, "output_dir": 出力先}
    """
    import os
    
    # 出力ディレクトリ作成
    os.makedirs(output_dir, exist_ok=True)
    
    # タイムライン情報取得
    timeline_info = self.get_timeline_info()
    
    # マーカー取得
    markers = self.get_markers(color_filter)
    
    if not markers:
        print("警告: マーカーが見つかりません")
        return {"success": 0, "failed": 0, "output_dir": output_dir}
    
    print(f"処理開始: {len(markers)}個のマーカー")
    
    # プレフィックス設定
    if not file_prefix:
        file_prefix = f"{self.project.GetName()}_"
    
    # 静止画を取得
    exported_stills = []
    success_count = 0
    failed_count = 0
    
    for i, (frame_id, marker_info) in enumerate(markers.items(), 1):
        try:
            # タイムコードを計算
            timecode = self.frame_to_timecode(
                int(frame_id),
                timeline_info["start_frame"],
                timeline_info["start_timecode"],
                timeline_info["fps"]
            )
            
            # 再生ヘッドを移動
            self.timeline.SetCurrentTimecode(timecode)
            
            # 静止画を取得
            still = self.timeline.GrabStill()
            
            # ラベルを設定（タイムコードをファイル名用に変換）
            tc_label = timecode.replace(":", "-")
            self.album.SetLabel(still, tc_label)
            
            exported_stills.append(still)
            success_count += 1
            
            print(f"[{i}/{len(markers)}] 取得: {tc_label} ({marker_info['color']})")
            
        except Exception as e:
            print(f"[{i}/{len(markers)}] エラー: Frame {frame_id} - {e}")
            failed_count += 1
    
    # 一括書き出し
    if exported_stills:
        print(f"\n書き出し中...")
        result = self.album.ExportStills(
            exported_stills, 
            output_dir, 
            file_prefix, 
            image_format
        )
        
        if result:
            # ファイルをリネーム（タイムコード付き）
            self._rename_files_with_timecode(
                output_dir, 
                file_prefix, 
                exported_stills,
                image_format
            )
            
            # Galleryをクリーンアップ
            self.album.DeleteStills(exported_stills)
            
            print(f"\n完了: {success_count}枚のフレームを書き出しました")
            print(f"出力先: {output_dir}")
        else:
            print("エラー: 書き出しに失敗しました")
            failed_count = len(exported_stills)
            success_count = 0
    
    return {
        "success": success_count,
        "failed": failed_count,
        "output_dir": output_dir
    }

def _rename_files_with_timecode(self, output_dir: str, prefix: str, 
                                stills: list, format: str):
    """書き出したファイルをタイムコード付きにリネーム"""
    import os
    
    for i, still in enumerate(stills):
        old_name = f"{prefix}{i+1:06d}.{format}"
        old_path = os.path.join(output_dir, old_name)
        
        if os.path.exists(old_path):
            label = self.album.GetLabel(still)
            new_name = f"{prefix}{label}_{i+1:03d}.{format}"
            new_path = os.path.join(output_dir, new_name)
            
            os.rename(old_path, new_path)
```

### 3. コマンドラインインターフェース

```python
def main():
    """メイン関数（CLI）"""
    import argparse
    import os
    
    parser = argparse.ArgumentParser(
        description='DaVinci Resolve マーカーフレーム書き出しツール'
    )
    parser.add_argument(
        '-o', '--output',
        default=os.path.expanduser("~/Desktop/marker_frames"),
        help='出力ディレクトリ (デフォルト: ~/Desktop/marker_frames)'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['png', 'jpg', 'tiff', 'dpx'],
        default='png',
        help='画像フォーマット (デフォルト: png)'
    )
    parser.add_argument(
        '-p', '--prefix',
        default='',
        help='ファイル名プレフィックス (デフォルト: プロジェクト名)'
    )
    parser.add_argument(
        '-c', '--color',
        help='マーカー色フィルター (例: Blue, Red)'
    )
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=95,
        help='JPEG品質 1-100 (デフォルト: 95)'
    )
    
    args = parser.parse_args()
    
    # Exporter初期化
    exporter = MarkerFrameExporter()
    
    # Resolveに接続
    if not exporter.connect_to_resolve():
        return 1
    
    # 書き出し実行
    result = exporter.export_all_markers(
        output_dir=args.output,
        file_prefix=args.prefix,
        image_format=args.format,
        color_filter=args.color
    )
    
    # 結果表示
    print("\n" + "="*50)
    print(f"成功: {result['success']}枚")
    print(f"失敗: {result['failed']}枚")
    print(f"出力先: {result['output_dir']}")
    print("="*50)
    
    return 0 if result['failed'] == 0 else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
```

---

## インストールスクリプト

### install.sh (macOS)

```bash
#!/bin/bash

echo "DaVinci Resolve マーカーフレーム書き出しツール - インストール"
echo "================================================================"

# 環境変数設定
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"

# 環境変数を.zshrcまたは.bash_profileに追加
SHELL_RC="$HOME/.zshrc"
if [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.bash_profile"
fi

echo "環境変数を $SHELL_RC に追加..."
echo "" >> "$SHELL_RC"
echo "# DaVinci Resolve Scripting API" >> "$SHELL_RC"
echo "export RESOLVE_SCRIPT_API=\"$RESOLVE_SCRIPT_API\"" >> "$SHELL_RC"
echo "export RESOLVE_SCRIPT_LIB=\"$RESOLVE_SCRIPT_LIB\"" >> "$SHELL_RC"
echo "export PYTHONPATH=\"\$PYTHONPATH:\$RESOLVE_SCRIPT_API/Modules/\"" >> "$SHELL_RC"

# スクリプトをResolveのUtilityフォルダにコピー
SCRIPT_DIR="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility"
echo "スクリプトを $SCRIPT_DIR にコピー..."
sudo mkdir -p "$SCRIPT_DIR"
sudo cp marker_frame_export.py "$SCRIPT_DIR/"
sudo chmod +x "$SCRIPT_DIR/marker_frame_export.py"

# Python依存関係をインストール
echo "Python依存関係をインストール..."
pip3 install -r requirements.txt

echo ""
echo "インストール完了！"
echo "DaVinci Resolveを再起動してください。"
echo "使用方法: Workspace > Scripts > Utility > marker_frame_export"
```

### install.bat (Windows)

```batch
@echo off
echo DaVinci Resolve マーカーフレーム書き出しツール - インストール
echo ================================================================

REM 環境変数設定
set RESOLVE_SCRIPT_API=%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting
set RESOLVE_SCRIPT_LIB=C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll
set PYTHONPATH=%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\

REM 環境変数を永続化
echo 環境変数を設定...
setx RESOLVE_SCRIPT_API "%RESOLVE_SCRIPT_API%"
setx RESOLVE_SCRIPT_LIB "%RESOLVE_SCRIPT_LIB%"
setx PYTHONPATH "%PYTHONPATH%"

REM スクリプトをResolveのUtilityフォルダにコピー
set SCRIPT_DIR=%APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Utility
echo スクリプトを %SCRIPT_DIR% にコピー...
if not exist "%SCRIPT_DIR%" mkdir "%SCRIPT_DIR%"
copy marker_frame_export.py "%SCRIPT_DIR%\"

REM Python依存関係をインストール
echo Python依存関係をインストール...
pip install -r requirements.txt

echo.
echo インストール完了！
echo DaVinci Resolveを再起動してください。
echo 使用方法: Workspace ^> Scripts ^> Utility ^> marker_frame_export
pause
```

---

## requirements.txt

```
# オプション: タイムコード変換ライブラリ
timecode>=1.4.0
```

---

## README.md（簡潔版）

```markdown
# DaVinci Resolve マーカーフレーム書き出しツール

DaVinci Resolveのタイムライン上のマーカー位置から、タイムコード情報付きでフレームを自動書き出しします。

## インストール

### macOS
```bash
chmod +x install.sh
./install.sh
```

### Windows
```cmd
install.bat
```

## 使用方法

### DaVinci Resolve内から
1. Resolveを起動
2. プロジェクトとタイムラインを開く
3. マーカーを配置
4. `Workspace` > `Scripts` > `Utility` > `marker_frame_export`

### コマンドライン
```bash
python marker_frame_export.py -o ~/Desktop/frames -f png
```

## オプション

- `-o, --output`: 出力ディレクトリ
- `-f, --format`: 画像フォーマット (png, jpg, tiff, dpx)
- `-p, --prefix`: ファイル名プレフィックス
- `-c, --color`: マーカー色フィルター

## 出力例

```
MyProject_01-23-45-12_001.png
MyProject_01-23-47-08_002.png
```
```

---

## 重要な実装ポイント

### 1. エラーハンドリング
- すべてのAPI呼び出しをtry-exceptで囲む
- ユーザーフレンドリーなエラーメッセージ
- ログ出力で詳細を記録

### 2. パフォーマンス
- 大量のマーカーでも安定動作
- 進捗表示で処理状況を可視化
- メモリ使用量を最小限に

### 3. クロスプラットフォーム
- パス処理は`os.path.join()`を使用
- 環境変数はOSごとに適切に設定
- ファイル名にOS非対応文字を使用しない

### 4. ユーザビリティ
- デフォルト値で即座に使える
- 明確なヘルプメッセージ
- 処理結果を明示的に表示

---

## テスト項目

- [ ] Resolve接続
- [ ] マーカー取得
- [ ] タイムコード変換
- [ ] フレーム書き出し
- [ ] ファイルリネーム
- [ ] 色フィルタリング
- [ ] エラーハンドリング
- [ ] クロスプラットフォーム動作

---

**実装時の注意事項**:
1. すべての文字列はUTF-8で処理
2. パスは絶対パスで指定
3. Resolveとの通信は同期的に実行
4. ユーザーに定期的にフィードバックを提供

このガイドに従って実装すれば、堅牢で使いやすいツールが完成します。
