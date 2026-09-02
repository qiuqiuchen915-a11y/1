# -*- coding: utf-8 -*-
"""图生图：拿单品截图 + 白底 prompt，生成电商白底单品图。

支持两家模型（见 references/whitebg-image-gen.md）：
  --provider gemini    nano-banana / Gemini 2.5 Flash Image（需 GEMINI_API_KEY）
  --provider seedream  火山引擎 Seedream 4.0（需 ARK_API_KEY）

用法：
  py generate_whitebg.py --provider seedream --image crops/02_print_dress.png \\
       --prompt "以参考图中的连衣裙为主体，纯白背景无模特，电商主图，保留印花面料细节" \\
       --out out/02_white.png

  py generate_whitebg.py --provider gemini --image crops/02_print_dress.png \\
       --prompt "Clean white-background e-commerce photo of the dress in the reference, no model" \\
       --out out/02_white.png --aspect 4:5 --size 2K

prompt 也可用 --prompt-file 从文件读（避免命令行转义麻烦，Windows 推荐）。
依赖按需安装：pip install pillow google-genai   /   pip install volcengine-python-sdk
"""
import os
import sys
import argparse
import base64
import mimetypes


def read_prompt(args):
    if args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    if args.prompt:
        return args.prompt
    sys.exit("错误：必须给 --prompt 或 --prompt-file")


# ---------- nano-banana / Gemini ----------
def gen_gemini(args, prompt):
    try:
        from google import genai
        from google.genai import types
        from PIL import Image
    except ImportError:
        sys.exit("缺依赖：pip install google-genai pillow")

    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("错误：未设置环境变量 GEMINI_API_KEY")

    client = genai.Client()
    ref = Image.open(args.image)

    resp = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt, ref],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=args.aspect,
                image_size=args.size,
            ),
        ),
    )

    if not getattr(resp, "parts", None):
        # 安全过滤可能导致 parts 为空
        fb = getattr(resp, "prompt_feedback", None)
        sys.exit(f"错误：没有返回图片，可能被安全过滤。prompt_feedback={fb}")

    saved = False
    for part in resp.parts:
        if getattr(part, "inline_data", None) is not None:
            part.as_image().save(args.out)
            saved = True
            break
    if not saved:
        sys.exit("错误：响应里没有图片部分（只有文本）")
    print(f"OK [gemini] -> {args.out}")


# ---------- Seedream / 火山方舟 ----------
def load_image_as_base64(path):
    mime, _ = mimetypes.guess_type(path)
    mime = (mime or "image/png").lower()
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def gen_seedream(args, prompt):
    try:
        from volcenginesdkarkruntime import Ark
    except ImportError:
        sys.exit("缺依赖：pip install volcengine-python-sdk")

    if not os.environ.get("ARK_API_KEY"):
        sys.exit("错误：未设置环境变量 ARK_API_KEY")

    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=os.environ.get("ARK_API_KEY"),
    )

    # Seedream 的 size 用像素串；把 1K/2K/4K 简单映射成方形像素
    size_map = {"1K": "1024x1024", "2K": "2048x2048", "4K": "4096x4096"}
    size = size_map.get(args.size, args.size if "x" in args.size else "2048x2048")

    resp = client.images.generate(
        model="doubao-seedream-4-0-250828",
        prompt=prompt,
        image=load_image_as_base64(args.image),
        size=size,
        response_format="url",
        watermark=False,
    )

    url = resp.data[0].url
    print(f"OK [seedream] 生成图 URL（24h 有效）: {url}")

    # 顺手下载转存（url 24h 失效）
    try:
        import urllib.request
        urllib.request.urlretrieve(url, args.out)
        print(f"已转存 -> {args.out}")
    except Exception as e:
        print(f"警告：自动下载失败，请手动保存 URL。原因：{e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", required=True, choices=["gemini", "seedream"])
    ap.add_argument("--image", required=True, help="参考图（单品截图）路径")
    ap.add_argument("--prompt", help="白底图 prompt")
    ap.add_argument("--prompt-file", help="从文件读 prompt（Windows 推荐，避免转义）")
    ap.add_argument("--out", required=True, help="输出图片路径")
    ap.add_argument("--aspect", default="1:1", help="Gemini 用：宽高比，如 1:1 / 4:5")
    ap.add_argument("--size", default="2K", help="分辨率 1K/2K/4K 或像素串如 2048x2048")
    args = ap.parse_args()

    prompt = read_prompt(args)
    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)

    if args.provider == "gemini":
        gen_gemini(args, prompt)
    else:
        gen_seedream(args, prompt)


if __name__ == "__main__":
    main()
