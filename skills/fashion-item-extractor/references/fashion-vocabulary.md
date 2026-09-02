# 时尚摄影 Prompt 参考词汇表

SKILL.md 需要写准服装、布光、模型差异时查这里。不用一次读完，按需查对应小节。

## 目录
- [服装品类与版型词](#服装品类与版型词)
- [面料与质感词](#面料与质感词)
- [颜色——说具体](#颜色说具体)
- [布光对照表](#布光对照表)
- [镜头与景别](#镜头与景别)
- [画质收尾词](#画质收尾词)
- [模特气质参考](#模特气质参考)
- [各模型 prompt 差异](#各模型-prompt-差异)
- [常见出图问题与对策](#常见出图问题与对策)

---

## 服装品类与版型词

写版型是为了让模型知道布料怎么垂、模特怎么站。

| 中文 | 英文 | 出图要点 |
|------|------|---------|
| Oversize / 廓形 | oversized, boxy, relaxed fit | 布料堆叠、垂坠感，模特别站太直 |
| 修身 / 合体 | slim fit, tailored, fitted | 贴合身形，展示线条 |
| 阔腿裤 | wide-leg trousers | 走动时摆动，站姿微开 |
| 直筒 | straight-cut | 利落垂直 |
| A 字 | A-line | 上窄下宽，转身时张开 |
| 收腰 | cinched waist, belted | 强调腰线 |
| 落肩 | drop-shoulder | 肩线下移，慵懒感 |

## 面料与质感词

面料是高级感的命门——它决定光怎么打、布怎么反光。

| 面料 | 英文 | 光线搭配 | 质感关键词 |
|------|------|---------|-----------|
| 真丝 | silk, satin | 侧光带高光 | lustrous, flowing, soft sheen |
| 雪纺 | chiffon | 逆光透光 | sheer, airy, translucent |
| 针织 | knit, ribbed | 柔光显纹理 | cozy, textured, chunky knit |
| 牛仔 | denim | 自然光/硬光 | rugged, washed, raw denim |
| 皮革 | leather | 硬光出高光 | glossy / matte, structured |
| 羊毛/呢 | wool, tweed | 柔和侧光 | warm, fuzzy, structured |
| 棉/府绸 | cotton, poplin | 均匀柔光 | crisp, clean, matte |
| 亮片/金属 | sequined, metallic | 多点光源 | shimmering, reflective |

## 颜色——说具体

模型最容易在颜色上跑偏。永远用"修饰词 + 颜色"而不是裸色名。

- 蓝：雾霾蓝 dusty blue / 藏青 navy / 克莱因蓝 klein blue / 婴儿蓝 baby blue
- 米/棕：燕麦色 oatmeal / 驼色 camel / 焦糖 caramel / 卡其 khaki
- 绿：橄榄绿 olive / 牛油果绿 / 墨绿 forest green / 薄荷 mint
- 红粉：酒红 burgundy / 砖红 brick / 裸粉 nude pink / 莓果色 berry
- 中性：象牙白 ivory / 炭灰 charcoal / 奶油白 cream / 雾灰 misty grey

## 布光对照表

| 布光 | 英文 | 效果 | 适用 |
|------|------|------|------|
| 柔光箱/均匀光 | soft diffused studio lighting | 平整、无硬阴影 | 电商棚拍 |
| 蝴蝶光 | butterfly lighting | 鼻下小阴影，显脸精致 | 美妆/正面 |
| 伦勃朗光 | Rembrandt lighting | 脸颊三角光，立体 | 人像、有质感的大片 |
| 黄金时刻 | golden hour backlight | 暖逆光、发丝光晕 | 街拍、生活感 |
| 硬光 | hard directional light | 强阴影、对比、戏剧 | 时尚大片、机能风 |
| 霓虹/环境色 | neon / colored ambient | 氛围、调性 | 都市夜景、Y2K |

## 镜头与景别

- **85mm f/1.4**：人像虚化，背景奶油化——电商半身/特写
- **50mm**：自然透视——通用
- **35mm**：带环境——街拍、大片全景
- **景别**：full-body shot 全身 / three-quarter 大半身 / waist-up 半身 / close-up 特写
- 展示裤型、鞋、长裙 → 必须 full-body；展示上衣面料/领口 → waist-up 即可

## 画质收尾词

- 通用：photorealistic, highly detailed, professional fashion photography, sharp focus
- 加分：editorial photography, shot on Hasselblad / Phase One, 8k, fine fabric detail
- 电商专用：clean product shot, even exposure, true-to-color, e-commerce catalog style

## 画幅 / 相机参数建议

出图最容易在画幅上翻车，prompt 里最好显式给一个比例：
- **电商主图**：3:4 竖图 或 1:1 方图
- **时尚大片**：4:5 或更竖的构图，给氛围留空间
- **白底单品图**（extractor 用）：1:1 方图最通用，鞋/包也可 4:3

相机/镜头参数可以让画质更稳、更像真实摄影（按场景挑，不用全堆）：
- 机身感：shot on Hasselblad / Phase One / full-frame DSLR
- 焦段：85mm 人像虚化 / 50mm 自然 / 35mm 带环境
- 光圈：电商单品图用 f/8–f/11 全幅清晰；人像大片用 f/1.8–f/2.8 浅景深虚化背景
- 注意：**单品白底商品图要 deep focus 全清晰，不要浅景深**；只有模特大片才用大光圈虚化

## 模特气质参考

用户没指定模特时，按衣服风格选并说明理由：
- 极简/高级 → 冷感、轮廓干净、克制神态
- 街头/Y2K → 年轻、有活力、随性
- 法式/复古 → 慵懒、自然、有故事感
- 学院/通勤 → 干净、亲和、精致
- 机能/暗黑 → 冷峻、有态度

模特设定要素：性别、大致年龄段、族裔/肤色、发型发色、身形、神态。**用户指定了就严格照用户的来，不要自作主张改。**

## 各模型 prompt 差异

| 模型 | 语言 | 风格 | 注意 |
|------|------|------|------|
| 即梦 Seedream | 中文优先 | 自然语言长描述 | 中文细节描述很吃，颜色面料写细 |
| 可图 Kolors | 中文优先 | 自然语言 | 同上，对中式审美/服饰友好 |
| nano-banana | 中英皆可 | 自然语言 | 擅长真实感和图生图编辑 |
| Gemini 系 | 英文更稳 | 自然语言，可结构化 | 英文 prompt 一致性更好 |
| Midjourney | 英文 | 关键词 + 参数 | 仅用户明确要时用：`--ar 3:4 --style raw --v 6` |

## 常见出图问题与对策

- **颜色跑偏** → 颜色写具体修饰词；必要时加 "true to the reference color"。
- **面料变廉价** → 点明面料名 + 质感词 + 配对的光线。
- **衣服细节丢失/变形** → 把关键细节（领型、纽扣、印花位置）单独描述清楚。
- **手指/姿态畸形** → 用正面描述"natural relaxed hands"，避免复杂手部动作。
- **背景抢戏** → 明确"clean background, focus on the outfit"。
- **整体塑料感** → 加真实皮肤纹理 natural skin texture、避免过度磨皮词。
