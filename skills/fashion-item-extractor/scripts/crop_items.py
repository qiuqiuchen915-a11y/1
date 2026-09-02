# -*- coding: utf-8 -*-
"""按 Claude 看图估算的比例坐标，把一张穿搭图里的各单品矩形裁剪出来。

用法：
    py crop_items.py <原图路径> <输出目录> <items_json>

items_json 是一个 JSON 字符串或 .json 文件路径，形如：
    [
      {"name": "01_outer_cardigan", "box": [0.18, 0.18, 0.82, 0.62]},
      {"name": "02_print_dress",    "box": [0.28, 0.22, 0.72, 0.58]}
    ]
box 是 [left, top, right, bottom]，用 0~1 比例表示（相对原图宽高）。
比例制让坐标与分辨率无关，Claude 看图后填比例即可，脚本自动换算像素。

设计取舍（见 SKILL.md）：矩形裁剪，会带一点背景，不做精准抠图。
作为"找同款/喂图编辑模型的视觉锚点"足够；要去背景另上抠图模型。
"""
import os
import sys
import json
from PIL import Image


def load_items(arg):
    """arg 可以是 JSON 字符串，也可以是 .json 文件路径。"""
    if os.path.isfile(arg):
        with open(arg, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.loads(arg)


def main():
    if len(sys.argv) < 4:
        print("用法: py crop_items.py <原图> <输出目录> <items_json>")
        sys.exit(1)

    src, out_dir, items_arg = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out_dir, exist_ok=True)

    im = Image.open(src).convert("RGB")
    W, H = im.size
    items = load_items(items_arg)

    results = []
    for it in items:
        name = it["name"]
        l, t, r, b = it["box"]
        box = (int(l * W), int(t * H), int(r * W), int(b * H))
        crop = im.crop(box)
        path = os.path.join(out_dir, name + ".png")
        crop.save(path)
        results.append({"name": name, "box_px": box, "size": crop.size, "path": path})
        print(f"{name}: box={box} size={crop.size} -> {path}")

    print(f"DONE. 共 {len(results)} 件，原图 {W}x{H}")
    return results


if __name__ == "__main__":
    main()
