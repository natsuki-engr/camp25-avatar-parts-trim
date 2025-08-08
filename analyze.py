#!/usr/bin/env python3
import os
import glob
import json
from PIL import Image, ImageDraw
import numpy as np

def get_bounding_box(image):
    """アルファ値が0でない部分の包括する四角形を取得"""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    data = np.array(image)
    alpha = data[:, :, 3]
    
    # アルファ値が0でない座標を取得
    coords = np.where(alpha > 0)
    
    if len(coords[0]) == 0:
        return None
    
    # 最小・最大座標を取得
    min_y, max_y = coords[0].min(), coords[0].max()
    min_x, max_x = coords[1].min(), coords[1].max()
    
    return (min_x, min_y, max_x, max_y)

def vertical_centralize_bounding_box(bbox, image_size):
    """四角を画像の中央に配置するように調整"""
    if bbox is None:
        return None
            
    width, height = image_size
    min_x, min_y, max_x, max_y = bbox

    left_space = min_x
    right_space = width - max_x

    if left_space > right_space:
        # 左側のスペースが大きい場合、左に伸ばす
        min_x = min_x - (left_space - right_space)
    else:
        # 右側のスペースが大きい場合、右に伸ばす
        max_x = max_x + (right_space - left_space)
        
    return (min_x, min_y, max_x, max_y)

def composite_images_in_directory(directory_path):
    """ディレクトリ内の画像を重ね合わせる"""
    image_files = glob.glob(os.path.join(directory_path, "*.png"))
    
    if not image_files:
        return None
    
    # 最初の画像をベースにする
    base_image = Image.open(image_files[0]).convert('RGBA')
    result = base_image.copy()
    
    # 残りの画像を重ね合わせる
    for image_file in image_files[1:]:
        overlay = Image.open(image_file).convert('RGBA')
        result = Image.alpha_composite(result, overlay)
    
    return result

def draw_bounding_box_on_image(image, bbox):
    """画像の中央に四角を描画した新しい画像を作成"""
    if bbox is None:
        return image
    
    # 新しい画像を作成（元画像をコピー）
    result = image.copy()
    draw = ImageDraw.Draw(result)
    
    # 四角形を描画（赤色、線幅2）
    draw.rectangle(bbox, outline='red', width=2)
    
    return result

def main():
    input_dir = "./input"
    output_dir = "./output/analyze"
    
    # outputディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 各サブディレクトリを処理
    subdirs = ['01-skin', '02-hair', '03-eye', '04-tops', '05-bottoms', '06-face-skin', '07-upper-skin', '08-lower-skin']
    
    coordinates_data = {}
    
    for subdir in subdirs:
        subdir_path = os.path.join(input_dir, subdir)
        
        if not os.path.exists(subdir_path):
            print(f"Warning: Directory {subdir_path} does not exist")
            continue
        
        print(f"Processing {subdir}...")
        
        # ディレクトリ内の画像を重ね合わせ
        composite_image = composite_images_in_directory(subdir_path)
        
        if composite_image is None:
            print(f"No images found in {subdir_path}")
            continue
        
        # アルファ値が0でない部分の包括する四角を取得
        bbox = get_bounding_box(composite_image)
        
        # 画像の中央に四角が配置されるよう四角を拡張
        # bbox = vertical_centralize_bounding_box(bbox, composite_image.size)
        
        # 四角を描画
        result_image = draw_bounding_box_on_image(composite_image, bbox)
        
        # 保存
        output_filename = f"{subdir}.png"
        output_path = os.path.join(output_dir, output_filename)
        result_image.save(output_path)
        
        print(f"Saved: {output_path}")
        if bbox:
            print(f"Bounding box: {bbox}")
            # 座標データを保存
            coordinates_data[subdir] = {
                "x": int(bbox[0]),
                "y": int(bbox[1]),
                "width": int(bbox[2] - bbox[0]),
                "height": int(bbox[3] - bbox[1])
            }
    
    # 座標データをJSONで保存
    json_path = os.path.join(output_dir, "coordinates.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(coordinates_data, f, indent=2, ensure_ascii=False)
    
    print(f"Coordinates saved to: {json_path}")

if __name__ == "__main__":
    main()