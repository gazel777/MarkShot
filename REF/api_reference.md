# DaVinci Resolve Scripting API リファレンス
## マーカーフレーム書き出しツール向け

---

## 必要なAPIメソッド一覧

### 1. 初期化・接続

#### DaVinciResolveScript.scriptapp()
```python
import DaVinciResolveScript as dvr_script
resolve = dvr_script.scriptapp("Resolve")
```
- **戻り値**: Resolve オブジェクト、または接続失敗時は None
- **説明**: DaVinci Resolve アプリケーションへの接続を確立

---

### 2. プロジェクト・タイムライン操作

#### Resolve.GetProjectManager()
```python
project_manager = resolve.GetProjectManager()
```
- **戻り値**: ProjectManager オブジェクト
- **説明**: プロジェクトマネージャーオブジェクトを取得

#### ProjectManager.GetCurrentProject()
```python
project = project_manager.GetCurrentProject()
```
- **戻り値**: Project オブジェクト、または開いているプロジェクトがない場合は None
- **説明**: 現在開いているプロジェクトを取得

#### Project.GetCurrentTimeline()
```python
timeline = project.GetCurrentTimeline()
```
- **戻り値**: Timeline オブジェクト、または開いているタイムラインがない場合は None
- **説明**: 現在開いているタイムラインを取得

#### Project.GetName()
```python
project_name = project.GetName()
```
- **戻り値**: string (プロジェクト名)
- **説明**: プロジェクト名を取得

---

### 3. タイムライン情報取得

#### Timeline.GetName()
```python
timeline_name = timeline.GetName()
```
- **戻り値**: string (タイムライン名)
- **説明**: タイムライン名を取得

#### Timeline.GetStartFrame()
```python
start_frame = timeline.GetStartFrame()
```
- **戻り値**: int (開始フレーム番号)
- **説明**: タイムラインの開始フレーム位置を取得

#### Timeline.GetStartTimecode()
```python
start_tc = timeline.GetStartTimecode()
```
- **戻り値**: string (タイムコード形式: "HH:MM:SS:FF")
- **説明**: タイムラインの開始タイムコードを取得
- **例**: "01:00:00:00"

#### Timeline.GetSetting(settingName)
```python
fps = timeline.GetSetting('timelineFrameRate')
```
- **引数**: 
  - `settingName` (string): 設定名
    - `'timelineFrameRate'`: フレームレート
    - `'timelineResolutionWidth'`: 解像度（幅）
    - `'timelineResolutionHeight'`: 解像度（高さ）
- **戻り値**: string または int (設定値)
- **説明**: タイムライン設定を取得
- **FPS例**: "23.976", "24", "25", "29.97", "30", "50", "59.94", "60"

---

### 4. マーカー操作

#### Timeline.GetMarkers()
```python
markers = timeline.GetMarkers()
```
- **戻り値**: dict (フレームID → マーカー情報の辞書)
- **構造**:
  ```python
  {
      frame_id (int): {
          "color": string,      # "Blue", "Cyan", "Green", "Yellow", 
                               # "Red", "Pink", "Purple", "Fuchsia", 
                               # "Rose", "Lavender", "Sky", "Mint", 
                               # "Lemon", "Sand", "Cocoa", "Cream"
          "name": string,       # マーカー名
          "note": string,       # マーカーメモ
          "duration": int,      # マーカー期間（フレーム数、デフォルト1）
          "customData": string  # カスタムデータ（オプション）
      }
  }
  ```
- **例**:
  ```python
  {
      100: {
          "color": "Blue",
          "name": "Important Scene",
          "note": "Check color grading",
          "duration": 1,
          "customData": ""
      },
      250: {
          "color": "Red",
          "name": "Action Shot",
          "note": "",
          "duration": 1,
          "customData": ""
      }
  }
  ```

#### Timeline.AddMarker(frameId, color, name, note, duration, customData)
```python
success = timeline.AddMarker(100, "Blue", "Test", "Note", 1, "")
```
- **引数**:
  - `frameId` (int): フレーム位置
  - `color` (string): マーカー色
  - `name` (string): マーカー名
  - `note` (string): メモ
  - `duration` (int): 期間（フレーム数）
  - `customData` (string): カスタムデータ（オプション）
- **戻り値**: Bool (成功時 True)
- **説明**: 新しいマーカーを追加

---

### 5. 再生ヘッド操作

#### Timeline.GetCurrentTimecode()
```python
current_tc = timeline.GetCurrentTimecode()
```
- **戻り値**: string (現在のタイムコード "HH:MM:SS:FF")
- **説明**: 現在の再生ヘッド位置をタイムコードで取得

#### Timeline.SetCurrentTimecode(timecode)
```python
success = timeline.SetCurrentTimecode("01:23:45:12")
```
- **引数**: 
  - `timecode` (string): タイムコード "HH:MM:SS:FF"
- **戻り値**: Bool (成功時 True)
- **説明**: 再生ヘッドを指定タイムコードに移動
- **重要**: マーカー位置でフレームを書き出す前にこれを実行

---

### 6. 静止画書き出し

#### Timeline.GrabStill()
```python
gallery_still = timeline.GrabStill()
```
- **戻り値**: GalleryStill オブジェクト
- **説明**: 現在の再生ヘッド位置のフレームをGalleryに静止画として取り込む
- **注意**: 
  - SetCurrentTimecode()で位置を設定してから実行
  - 書き出しには別途ExportStills()が必要

#### Timeline.GrabAllStills(stillFrameSource)
```python
stills = timeline.GrabAllStills(1)  # 1=最初のフレーム, 2=中間フレーム
```
- **引数**: 
  - `stillFrameSource` (int): 
    - `1` = 各クリップの最初のフレーム
    - `2` = 各クリップの中間フレーム
- **戻り値**: list of GalleryStill オブジェクト
- **説明**: タイムライン上の全クリップから静止画を取得

---

### 7. Gallery操作

#### Project.GetGallery()
```python
gallery = project.GetGallery()
```
- **戻り値**: Gallery オブジェクト
- **説明**: プロジェクトのGalleryオブジェクトを取得

#### Gallery.GetCurrentStillAlbum()
```python
album = gallery.GetCurrentStillAlbum()
```
- **戻り値**: GalleryStillAlbum オブジェクト
- **説明**: 現在のスチルアルバムを取得

#### Gallery.GetAlbumName(galleryStillAlbum)
```python
album_name = gallery.GetAlbumName(album)
```
- **引数**: 
  - `galleryStillAlbum` (GalleryStillAlbum): アルバムオブジェクト
- **戻り値**: string (アルバム名)
- **説明**: アルバム名を取得

#### Gallery.SetAlbumName(galleryStillAlbum, albumName)
```python
success = gallery.SetAlbumName(album, "My Stills")
```
- **引数**: 
  - `galleryStillAlbum` (GalleryStillAlbum): アルバムオブジェクト
  - `albumName` (string): 新しいアルバム名
- **戻り値**: Bool (成功時 True)
- **説明**: アルバム名を設定

---

### 8. GalleryStillAlbum操作

#### GalleryStillAlbum.GetStills()
```python
stills = album.GetStills()
```
- **戻り値**: list of GalleryStill オブジェクト
- **説明**: アルバム内の全静止画を取得

#### GalleryStillAlbum.GetLabel(galleryStill)
```python
label = album.GetLabel(still)
```
- **引数**: 
  - `galleryStill` (GalleryStill): 静止画オブジェクト
- **戻り値**: string (ラベル)
- **説明**: 静止画のラベルを取得

#### GalleryStillAlbum.SetLabel(galleryStill, label)
```python
success = album.SetLabel(still, "Scene_01")
```
- **引数**: 
  - `galleryStill` (GalleryStill): 静止画オブジェクト
  - `label` (string): 新しいラベル
- **戻り値**: Bool (成功時 True)
- **説明**: 静止画にラベルを設定
- **用途**: タイムコードをラベルとして設定可能

#### GalleryStillAlbum.ExportStills(galleryStillList, folderPath, filePrefix, format)
```python
success = album.ExportStills(
    [still1, still2],
    "/Users/username/Desktop/frames",
    "MyProject_",
    "png"
)
```
- **引数**: 
  - `galleryStillList` (list): 書き出す静止画のリスト
  - `folderPath` (string): 書き出し先ディレクトリの絶対パス
  - `filePrefix` (string): ファイル名プレフィックス
  - `format` (string): 画像フォーマット
    - 対応フォーマット: `"dpx"`, `"cin"`, `"tif"`, `"jpg"`, `"png"`, `"ppm"`, `"bmp"`, `"xpm"`
- **戻り値**: Bool (成功時 True、失敗時 False)
- **説明**: 静止画をファイルとして書き出し
- **ファイル名**: `{filePrefix}{連番}.{format}`
  - 例: `MyProject_000001.png`
- **注意**: 
  - 連番は自動付与（カスタマイズ不可）
  - タイムコードをファイル名に含めるには、書き出し後にリネームが必要

#### GalleryStillAlbum.DeleteStills(galleryStillList)
```python
success = album.DeleteStills([still1, still2])
```
- **引数**: 
  - `galleryStillList` (list): 削除する静止画のリスト
- **戻り値**: Bool (成功時 True)
- **説明**: 静止画をアルバムから削除

---

## タイムコード変換ロジック

### フレーム → タイムコード変換

```python
def frame_to_timecode(frame: int, start_frame: int, start_timecode: str, fps: float) -> str:
    """
    フレーム番号をタイムコードに変換
    
    Args:
        frame: 対象フレーム番号
        start_frame: タイムライン開始フレーム
        start_timecode: タイムライン開始タイムコード "HH:MM:SS:FF"
        fps: フレームレート
    
    Returns:
        タイムコード文字列 "HH:MM:SS:FF"
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
    if frames >= fps:
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

### タイムコード → フレーム変換

```python
def timecode_to_frame(timecode: str, start_frame: int, start_timecode: str, fps: float) -> int:
    """
    タイムコードをフレーム番号に変換
    
    Args:
        timecode: 対象タイムコード "HH:MM:SS:FF"
        start_frame: タイムライン開始フレーム
        start_timecode: タイムライン開始タイムコード "HH:MM:SS:FF"
        fps: フレームレート
    
    Returns:
        フレーム番号
    """
    def tc_to_seconds(tc: str, fps: float) -> float:
        h, m, s, f = map(int, tc.replace(';', ':').split(':'))
        return h * 3600 + m * 60 + s + f / fps
    
    target_seconds = tc_to_seconds(timecode, fps)
    start_seconds = tc_to_seconds(start_timecode, fps)
    
    frame_diff = int((target_seconds - start_seconds) * fps)
    return start_frame + frame_diff
```

---

## 実装例: 基本的なマーカーフレーム書き出し

```python
#!/usr/bin/env python3
import os
import DaVinciResolveScript as dvr_script

def export_marker_frames():
    # 1. Resolveに接続
    resolve = dvr_script.scriptapp("Resolve")
    if not resolve:
        print("エラー: DaVinci Resolveが起動していません")
        return False
    
    # 2. プロジェクトとタイムラインを取得
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        print("エラー: プロジェクトが開かれていません")
        return False
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("エラー: タイムラインが開かれていません")
        return False
    
    # 3. タイムライン情報を取得
    project_name = project.GetName()
    start_frame = timeline.GetStartFrame()
    start_tc = timeline.GetStartTimecode()
    fps_str = timeline.GetSetting('timelineFrameRate')
    fps = float(fps_str) if fps_str != "23.976" else 23.976
    
    # 4. マーカーを取得
    markers = timeline.GetMarkers()
    if not markers:
        print("警告: マーカーが見つかりません")
        return False
    
    print(f"マーカー数: {len(markers)}")
    
    # 5. Gallery設定
    gallery = project.GetGallery()
    album = gallery.GetCurrentStillAlbum()
    
    # 6. 出力ディレクトリを作成
    output_dir = os.path.expanduser("~/Desktop/marker_frames")
    os.makedirs(output_dir, exist_ok=True)
    
    # 7. 各マーカー位置でフレームを書き出し
    exported_stills = []
    
    for frame_id, marker_info in markers.items():
        # タイムコードを計算
        timecode = frame_to_timecode(int(frame_id), start_frame, start_tc, fps)
        
        # 再生ヘッドを移動
        timeline.SetCurrentTimecode(timecode)
        
        # 静止画を取得
        still = timeline.GrabStill()
        
        # ラベルを設定（タイムコード）
        tc_label = timecode.replace(":", "-")
        album.SetLabel(still, tc_label)
        
        exported_stills.append(still)
        
        print(f"取得: Frame {frame_id} -> {timecode} ({marker_info['color']})")
    
    # 8. 一括書き出し
    file_prefix = f"{project_name}_"
    success = album.ExportStills(exported_stills, output_dir, file_prefix, "png")
    
    if success:
        print(f"\n完了: {len(exported_stills)}枚のフレームを書き出しました")
        print(f"出力先: {output_dir}")
        
        # 9. ファイルをリネーム（タイムコード付き）
        rename_files_with_timecode(output_dir, file_prefix, album, exported_stills)
        
        # 10. Galleryをクリーンアップ
        album.DeleteStills(exported_stills)
        return True
    else:
        print("エラー: 書き出しに失敗しました")
        return False

def rename_files_with_timecode(output_dir, prefix, album, stills):
    """書き出したファイルをタイムコード付きにリネーム"""
    for i, still in enumerate(stills):
        old_name = f"{prefix}{i+1:06d}.png"
        old_path = os.path.join(output_dir, old_name)
        
        label = album.GetLabel(still)
        new_name = f"{prefix}{label}_{i+1:03d}.png"
        new_path = os.path.join(output_dir, new_name)
        
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"リネーム: {old_name} -> {new_name}")

if __name__ == "__main__":
    export_marker_frames()
```

---

## 重要な注意点

### 1. ExportStills()の制限
- ファイル名は `{prefix}{連番}.{format}` 形式のみ
- 連番は自動で6桁（000001, 000002...）
- カスタムファイル名は書き出し後にリネームが必要

### 2. タイムコードの扱い
- API内部では "HH:MM:SS:FF" (コロン区切り)
- ファイル名には使用できないため、ハイフンに変換 "HH-MM-SS-FF"

### 3. GrabStill()のタイミング
- `SetCurrentTimecode()`の直後に実行
- Resolveがフレームをレンダリングする時間が必要な場合がある
- 大量処理時は短いsleep()を入れると安定

### 4. Galleryの管理
- 書き出し後は `DeleteStills()` でクリーンアップ推奨
- Galleryが満杯になると動作が不安定になる

### 5. フレームレート
- `"23.976"` は文字列として返される
- 計算時は float(23.976) として扱う

---

## トラブルシューティング

### ExportStills()が失敗する

**原因**:
- 書き出し先ディレクトリが存在しない
- 書き込み権限がない
- Galleryが空

**解決策**:
```python
# ディレクトリを事前作成
os.makedirs(output_dir, exist_ok=True)

# 権限をチェック
if not os.access(output_dir, os.W_OK):
    print(f"エラー: 書き込み権限がありません: {output_dir}")
```

### タイムコードがずれる

**原因**:
- フレームレートの扱いが不正確
- ドロップフレーム/ノンドロップフレームの混在

**解決策**:
```python
# FPS文字列を正確に変換
fps_map = {
    "23.976": 23.976,
    "24": 24.0,
    "25": 25.0,
    "29.97": 29.97,
    "30": 30.0,
    "50": 50.0,
    "59.94": 59.94,
    "60": 60.0
}
fps = fps_map.get(fps_str, float(fps_str))
```

### マーカーが取得できない

**原因**:
- タイムラインマーカーではなくクリップマーカー
- タイムラインが選択されていない

**解決策**:
```python
# タイムライン確認
timeline = project.GetCurrentTimeline()
if not timeline:
    print("タイムラインを開いてください")
    return

# マーカー確認
markers = timeline.GetMarkers()
if not markers:
    print("タイムラインマーカーが見つかりません")
    print("クリップマーカーは非対応です")
```

---

**参考資料**:
- [公式 DaVinci Resolve Scripting Documentation](https://www.blackmagicdesign.com/support/)
- [Formatted API Doc by X-Raym](https://extremraym.com/cloud/resolve-scripting-doc/)
- [BMD Forum - Scripting Section](https://forum.blackmagicdesign.com/viewforum.php?f=21)
