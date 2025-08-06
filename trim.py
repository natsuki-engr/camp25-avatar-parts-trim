#!/usr/bin/env python3
import os
import json
import glob
from PIL import Image

def load_coordinates(json_path):
    """coordinates.jsonから座標情報を読み込む"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_path} not found. Please run analyze.py first.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        return None

def trim_image(image_path, bbox_info, output_path):
    """画像をトリミングして保存"""
    try:
        # 画像を開く
        image = Image.open(image_path).convert('RGBA')
        
        # トリミング範囲を取得
        x = bbox_info['x']
        y = bbox_info['y']
        width = bbox_info['width']
        height = bbox_info['height']
        
        # トリミング実行
        cropped = image.crop((x, y, x + width, y + height))
        
        # 保存
        cropped.save(output_path)
        print(f"Trimmed: {image_path} -> {output_path}")
        
    except Exception as e:
        print(f"Error trimming {image_path}: {e}")

def trim_images_in_directory(input_dir, output_dir, bbox_info):
    """ディレクトリ内の全画像をトリミング"""
    image_files = glob.glob(os.path.join(input_dir, "*.png"))
    
    if not image_files:
        print(f"No PNG files found in {input_dir}")
        return
    
    for image_file in image_files:
        # 出力ファイル名を生成
        filename = os.path.basename(image_file)
        output_path = os.path.join(output_dir, filename)
        
        # トリミング実行
        trim_image(image_file, bbox_info, output_path)

def main():
    input_dir = "./input"
    coordinates_file = "./output/analyze/coordinates.json"
    output_dir = "./output/trim"
    
    # 座標情報を読み込み
    coordinates_data = load_coordinates(coordinates_file)
    if coordinates_data is None:
        return
    
    # outputディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 各カテゴリを処理
    for category, bbox_info in coordinates_data.items():
        print(f"Processing {category}...")
        
        # 入力ディレクトリのパス
        category_input_dir = os.path.join(input_dir, category)
        
        if not os.path.exists(category_input_dir):
            print(f"Warning: Directory {category_input_dir} does not exist")
            continue
        
        # カテゴリ別の出力ディレクトリを作成
        category_output_dir = os.path.join(output_dir, category)
        os.makedirs(category_output_dir, exist_ok=True)
        
        # ディレクトリ内の画像をトリミング
        trim_images_in_directory(category_input_dir, category_output_dir, bbox_info)
    
    print("Trimming completed!")

if __name__ == "__main__":
    main()