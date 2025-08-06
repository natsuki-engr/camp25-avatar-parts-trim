# 画像編集

## input

`./input`ディレクトリに元となる画像が配置されています。

ディレクトリ構成

```
input/
├── 01-skin
├── 02-hair
├── 03-eye
├── 04-tops
├── 05-bottoms
```

## analyze

- `analyze.py`は上記のディレクトリ内の画像を、ディレクトリ単位で重ね合わせた画像を１枚ずつ作成する
- さらに、ピクセルのアルファ値が0でない部分を包括する四角を描画する
- その四角は元画像の中央に配置される
- 作成した画像はoutput/analyzeディレクトリに保存される
- 描画した四角の座標と幅と高さを`output/analyze/coordinates.json`に保存する

## trim

- output/analyze/coordinates.jsonを読み込み、四角の座標と幅と高さを元に、`input`ディレクトリ内の画像をトリミングする
- トリミングした画像は`output/trim`ディレクトリに保存される
