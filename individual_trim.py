#!/usr/bin/env python3
import os
import glob
from PIL import Image
import numpy as np

def get_tight_bounding_box(image):
    """アルファ値が0でない部分の最小包括四角形を取得"""
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
    
    return (min_x, min_y, max_x + 1, max_y + 1)

def trim_image(image, bbox):
    """画像を指定された範囲でトリミング"""
    if bbox is None:
        return image
    
    min_x, min_y, max_x, max_y = bbox
    return image.crop((min_x, min_y, max_x, max_y))

def process_images_in_directory(input_dir, output_dir):
    """ディレクトリ内の画像を個別にトリミング"""
    image_files = glob.glob(os.path.join(input_dir, "*.png"))
    
    if not image_files:
        print(f"No images found in {input_dir}")
        return
    
    # 出力ディレクトリのサブディレクトリを作成
    subdir_name = os.path.basename(input_dir)
    output_subdir = os.path.join(output_dir, subdir_name)
    os.makedirs(output_subdir, exist_ok=True)
    
    for image_file in image_files:
        # 画像を読み込み
        image = Image.open(image_file).convert('RGBA')
        
        # 最小包括四角形を取得
        bbox = get_tight_bounding_box(image)
        
        if bbox is None:
            print(f"Warning: No visible content in {image_file}")
            continue
        
        # 画像をトリミング
        trimmed_image = trim_image(image, bbox)
        
        # 出力ファイル名を作成
        filename = os.path.basename(image_file)
        output_path = os.path.join(output_subdir, filename)
        
        # トリミングした画像を保存
        trimmed_image.save(output_path)
        
        print(f"Trimmed and saved: {output_path}")
        print(f"  Original size: {image.size}")
        print(f"  Trimmed size: {trimmed_image.size}")
        print(f"  Bounding box: {bbox}")

def main():
    input_dir = "./input"
    output_dir = "./output/individual_trim"
    
    # outputディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 各サブディレクトリを処理
    subdirs = ['01-skin', '02-hair', '03-eye', '04-tops', '05-bottoms', '06-face-skin', '07-upper-skin', '08-lower-skin']
    
    for subdir in subdirs:
        subdir_path = os.path.join(input_dir, subdir)
        
        if not os.path.exists(subdir_path):
            print(f"Warning: Directory {subdir_path} does not exist")
            continue
        
        print(f"\nProcessing {subdir}...")
        process_images_in_directory(subdir_path, output_dir)

if __name__ == "__main__":
    main()