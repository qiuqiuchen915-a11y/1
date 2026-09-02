# 生成电商白底图 — nano-banana / Seedream 图生图 API 参考

> 用途：拿「单品截图（crop_items.py 裁出来的实拍锚点）」+「白底单品 prompt」，调图生图模型，**真正生成出干净的电商白底单品图**。截图是视觉锚点（保款式/颜色/面料），prompt 是文字指令（去背景、白底、无模特）。两者一起喂 → 1:1 还原原图那件。
>
> 核实日期 2026-06-06，来源 URL 见各节末尾。模型版本号/价格会变，照抄前到官方控制台对一眼。

本 skill 配套脚本 `scripts/generate_whitebg.py` 已实现两家调用，命令行直接跑。本文是脚本背后的接口依据 + 手写调用时的参照。

---

## 选哪个模型

| | nano-banana (Gemini 2.5 Flash Image) | Seedream 4.0 |
|---|---|---|
| 平台 | Google 官方 Gemini API | 火山引擎方舟 Ark |
| 适合 | 英文 prompt 更稳、出图质感强、国际网络 | 中文 prompt 原生友好、国内网络稳、便宜 |
| 单价 | ~$0.039 / 张 | 0.20 元 / 张 |
| 水印 | **强制** SynthID 隐形水印（去不掉） | 可 `watermark=False` 关掉 |
| 默认推荐 | 海外/英文 prompt | **国内默认走这个**（中文 prompt + 便宜 + 可关水印） |

两家都做的是同一件事：**图生图**——参考图 + 文字 → 新图。白底单品场景两家都胜任，按网络环境和语言选。

---

## A. nano-banana (Gemini 2.5 Flash Image)

**模型 ID**：`gemini-2.5-flash-image`（已 GA；旧的 `-preview` 已废弃，别用）。
**SDK**：新 SDK `google-genai`，`pip install google-genai pillow`。**不是**旧的 `google-generativeai`。
**鉴权**：在 https://aistudio.google.com/apikey 拿 key，环境变量 `GEMINI_API_KEY`（`genai.Client()` 不传参时自动读）。REST 头是 `x-goog-api-key`。

### 图生图（Python，官方写法）
```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()  # 读 GEMINI_API_KEY
ref = Image.open("garment_crop.png")  # 单品截图（带背景没关系）

prompt = (
    "Generate a clean e-commerce product photo of the garment in the reference image. "
    "Pure white background (#FFFFFF), no model, no mannequin, item centered, soft even "
    "studio lighting, sharp all-over focus, true-to-reference color and texture."
)

resp = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt, ref],          # 文字 + PIL.Image，顺序无所谓
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="1:1", image_size="2K"),
    ),
)

for part in resp.parts:             # 文字和图可能交错，要遍历
    if part.inline_data is not None:
        part.as_image().save("white_bg.png")
```

### 参数
- `aspect_ratio`：`21:9 16:9 4:3 3:2 1:1 9:16 3:4 2:3 5:4 4:5`。单品白底用 `1:1`，时尚竖图用 `4:5`。有输入图时不写则跟随输入图比例。
- `image_size`：`"1K"`(默认) `"2K"` `"4K"`，**大写 K**。
- **每次只出 1 张**（没有 n 参数，要多张就循环）。**最多接受 10 张参考图**。

### 坑
- 每张图带**隐形 SynthID 水印**，去不掉——要无水印资产就别用这家。
- 被安全过滤拦时 `resp.parts` 可能为空，取图前要判空别崩。看 `resp.prompt_feedback` / `candidate.finish_reason`（`IMAGE_SAFETY`/`SAFETY`）。
- 复杂修图（"再去掉这个阴影"）官方建议多轮对话：把返回图再喂回去当下一轮输入。

来源：
- 模型页 https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image
- 图像生成 https://ai.google.dev/gemini-api/docs/image-generation
- 价格 https://ai.google.dev/gemini-api/docs/pricing
- GA/比例公告 https://developers.googleblog.com/gemini-2-5-flash-image-now-ready-for-production-with-new-aspect-ratios/

---

## B. Seedream 4.0（火山引擎方舟 Ark）

**模型 ID**：`doubao-seedream-4-0-250828`（4.0，原生支持图生图/多图融合；日期后缀是 id 一部分必须带全，以控制台显示为准，新版本会换后缀）。3.0 时代文生图(`seedream-3-0-t2i-*`)和图生图(`doubao-seededit-3-0-i2i`)是分开的两个模型，4.0 统一了，优先 4.0。
**SDK**：`pip install volcengine-python-sdk` → `from volcenginesdkarkruntime import Ark`。
**鉴权**：方舟控制台 https://console.volcengine.com/ark/ 拿 API Key，环境变量 `ARK_API_KEY`（不传时 SDK 自动读），HTTP 头 `Authorization: Bearer`。
**Endpoint**（国内）：`https://ark.cn-beijing.volces.com/api/v3/images/generations`。

### 图生图（Python，官方写法）
```python
import os, base64, mimetypes
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

def load_image_as_base64(path):
    mime, _ = mimetypes.guess_type(path)
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"   # 前缀必须全，格式名小写

resp = client.images.generate(
    model="doubao-seedream-4-0-250828",
    prompt="以参考图中的服装单品为主体，生成纯白背景、无模特、电商主图风格的单品平铺图，"
           "保留款式/颜色/面料细节，去除杂乱背景",
    image=load_image_as_base64("garment_crop.png"),  # 单图；多图传 list
    size="2048x2048",
    response_format="url",
    watermark=False,        # 显式关，别依赖默认（不同文档默认值口径不一）
    seed=12345,             # 可选，复现用
)
print(resp.data[0].url)     # url 模式：链接 24 小时有效，要及时转存
```

### 参数
- `size`：预设 `"1K"`~`"4K"` 或自定义像素 `"2048x2048"`。4.0 输出像素范围约 [1280×720, 4096×4096]。
- `response_format`：`"url"`(默认，24h 有效) 或 `"b64_json"`(纯 base64，无 data 前缀)。
- `watermark`：**永远显式传 `False`**，不要靠默认。
- `seed`：同模型+同 prompt+同 seed 可复现。
- 多张输出不用 OpenAI 的 `n`，用 `sequential_image_generation="auto"` + `sequential_image_generation_options={"max_images": N}`。
- 多图输入：4.0 支持 2~5 张参考图融合（输入+输出总数 ≤ 15）。

### 坑
- `image` base64 必须带 `data:image/jpeg;base64,` 全前缀、格式名小写，漏了/大写会报错。
- url 模式链接 **24 小时失效**，必须及时下载转存。
- 有内容审核，违规 prompt/图会被拦。
- IPM(每分钟图片数)量级 ~500，精确配额看控制台。

来源：
- 模型列表 https://www.volcengine.com/docs/82379/1330310
- Seedream 4.0 https://www.volcengine.com/docs/82379/1824718
- 价格 https://www.volcengine.com/docs/82379/1544106
- 官方 SDK https://github.com/volcengine/volcengine-python-sdk
- BytePlus 教程(国际站同套 API) https://docs.byteplus.com/en/docs/ModelArk/1824692

> 标「未二次核实」需自查的：Seedream 水印默认值、精确价格分档、内容审核细则、QPS 配额、账号实际可见的 model id 日期后缀。

---

## prompt 写法（白底图生图）

图生图时 prompt 的活和纯文生图不一样——参考图已经给了款式/颜色/面料，**prompt 重点变成"指令性的去背景 + 摆放 + 布光"**，而不是重新描述单品（重复描述反而可能和参考图打架）。建议结构：

1. **锚定参考图**：「以参考图中的[单品]为主体」/「the garment in the reference image」
2. **要什么背景**：纯白无缝 `#FFFFFF`、无模特、无人体、无衣架（或挂拍，看品类）
3. **摆放与布光**：居中、平铺/挂拍、均匀柔光、电商主图风格
4. **保真要求**：保留原款式/颜色/面料/印花/细节，去除原图杂乱背景与人体
5. **画质收尾**：全幅清晰、不要浅景深虚化、true-to-color、高细节

中文模型（Seedream）走中文 prompt，Gemini 走英文更稳。fashion-item-extractor 主流程生成的那段「白底单品 prompt」可直接复用作这里的指令主体，前面补一句「以参考图为主体」即可。
