---
name: rhinestone-preservation
description: 专用于服装图片中水晶烫钻的高保真识别、记录、保留与局部修复。采用多阶段流程：先裁切放大烫钻区域，区分真实水晶烫钻与格纹交点、印花点、面料高光，建立数量/坐标/间距/尺寸账本，再生成锁定服装底图并对烫钻区域做局部二次修复，逐区域放大比对；失败时只重做错误区域。烫钻作为独立立体辅料层，优先级高于去褶皱、版型对称和整体美化。原图无法可靠辨认时必须停止推测并要求补充微距参考图。
---

# rhinestone-preservation

## Purpose

这是一个针对服装商品图中 **水晶烫钻（rhinestone / hot-fix crystal）** 的专用高保真保护 Skill。

它不是普通的“保留细节”提示词，而是一套必须按顺序执行的 **检测 → 建账 → 锁底图 → 局部修复 → 放大复核 → 区域级返工** 多阶段工作流。

目标是最大限度避免以下常见错误：

- 烫钻在生成或精修后消失
- 烫钻数量减少或增加
- 烫钻位置移动
- 烫钻间距改变
- 烫钻大小改变
- 烫钻被识别成格纹交点
- 烫钻被识别成黑点、白点或印花点
- 烫钻被磨平成普通高光
- 烫钻变成亮片、噪点、星点或随机闪光
- 烫钻随着去褶皱、版型优化或纹理重绘而被抹掉

---

## Invocation

当用户明确说以下任意表达时，优先调用本 Skill：

- `$rhinestone-preservation`
- “保护烫钻”
- “烫钻不能丢”
- “保留水晶钻位置和数量”
- “格纹上的烫钻不能变白点”
- “精修这件带烫钻的衣服”
- “按原图保留烫钻”
- “烫钻局部修复”

若任务同时涉及 `fashion-flatlay-retouch`、`item-repair`、`clothing-detail` 等服装精修 Skill，本 Skill 对 **烫钻相关决策拥有更高优先级**。

---

# Absolute Priority Rule

## 烫钻是独立立体辅料层，不属于面料纹理

必须始终把烫钻理解为：

> **附着在面料表面的独立、凸起、具有真实厚度和切面的水晶/玻璃辅料层。**

烫钻不是：

- 格纹交点
- 印花图案
- 黑点
- 白点
- 波点
- 面料纤维亮点
- 高光噪点
- 数码锐化产生的亮边
- 提花纹理
- 面料反射纹理

任何步骤都不得把烫钻并入“面料纹理层”统一重绘。

---

## Priority Order

发生冲突时，严格按以下优先级处理：

1. **烫钻身份、数量、坐标、间距、大小、材质保持**
2. 商品原始结构与关键辅料保持
3. 格纹 / 图案 / 刺绣 / 蕾丝等身份保持
4. 面料真实纹理保持
5. 颜色与曝光一致性
6. 去褶皱
7. 版型左右对称
8. 轮廓美化
9. 整体“更好看”的审美优化

### 强制规则

如果“去褶皱、版型对称、整体美化”会造成烫钻：

- 消失
- 移动
- 数量变化
- 变形
- 被拉伸
- 被磨平
- 变成白点/黑点

则 **必须放弃该项美化**，优先保留烫钻。

---

# Input Requirements

## Minimum Input

至少需要：

- 一张能够看到服装烫钻区域的原始图片。

## Strongly Recommended

若有以下参考，应全部利用：

- 烫钻局部微距图
- 同款商品的高清细节图
- 正面 / 背面不同角度图
- 斜光下能够看见水晶切面反射的照片
- 用户指定的烫钻材质参考图

---

# Hard Stop Rule — 禁止猜测

当原图中的烫钻无法可靠判断时，必须停止推测。

以下任一情况触发 **STOP / REQUEST MACRO REFERENCE**：

- 原图分辨率不足，无法区分烫钻与格纹交点
- JPEG 压缩严重，亮点边缘已糊掉
- 烫钻区域严重过曝
- 烫钻区域严重欠曝
- 大面积被褶皱、头发、手、饰物或其他物体遮挡
- 无法确定某亮点究竟是水晶、印花点还是高光
- 无法确定烫钻数量
- 无法确定烫钻排列规律
- 不同参考图之间烫钻位置存在冲突且无法判断哪张为准

此时不得“合理补齐”、不得按照对称关系猜测、不得自动生成相似分布。

必须明确要求用户补充：

> **同一区域的高清烫钻微距参考图，尽量正视、对焦清晰、避免过曝。**

---

# Rhinestone Identity Model

在任何修图或生成前，先把候选亮点分成以下类别：

### A. TRUE_RHINESTONE
真实水晶烫钻。

典型特征：

- 位于面料表面而非织纹内部
- 有微小凸起或边缘厚度
- 存在水晶/玻璃切面
- 高光具有方向性
- 常同时出现亮面与较暗切面
- 随局部光线变化会产生折射/反射差异
- 与面料底纹存在明确的“贴附关系”

### B. PLAID_INTERSECTION
格纹经纬线交叉产生的交点。

典型特征：

- 与格线结构严格重合
- 无独立凸起
- 无晶体切面
- 大量重复且与格纹周期完全一致
- 颜色通常来自格线本身

### C. PRINT_DOT_BLACK
黑色印花点 / 图案点。

典型特征：

- 平面
- 无独立高光切面
- 边缘属于印刷/染色图案
- 不表现透明折射

### D. PRINT_DOT_WHITE
白色印花点 / 浅色图案点。

典型特征同上，不得因“亮”而误判为水晶。

### E. FABRIC_SPECULAR
面料自身高光。

典型特征：

- 通常沿纤维、褶皱或织纹方向延伸
- 形状会随布面曲率变化
- 不具有独立圆形/多面体辅料边界

### F. UNKNOWN
无法可靠判断的候选点。

任何 `UNKNOWN` 都不得自动升级为 `TRUE_RHINESTONE`。

---

# Mandatory Multi-Stage Workflow

必须按以下阶段执行。禁止直接跳到整件服装重绘。

---

## Stage 0 — Source Integrity Check

### 目标
确认原图是否足够支持烫钻级别的精修。

### 执行

1. 确认服装主体。
2. 找出所有可能存在烫钻的面料区域。
3. 判断每个区域清晰度。
4. 判断是否存在过曝、遮挡、压缩、运动模糊。
5. 标记：`PASS / UNCERTAIN / FAIL`。

### Gate 0

- `PASS` → 进入 Stage 1。
- `UNCERTAIN` → 可以继续分析，但所有不确定点必须进入 `UNKNOWN`。
- `FAIL` → 停止，不生成，要求微距参考图。

---

## Stage 1 — Crop & Magnify Rhinestone ROIs

### 目标
单独裁切、放大所有烫钻候选区域，不直接依赖整图缩略视图判断。

### 执行要求

将服装划分为多个 `ROI`（Region of Interest），例如：

- `R01_upper_left`
- `R02_upper_center`
- `R03_upper_right`
- `R04_mid_left`
- `R05_mid_center`
- `R06_mid_right`
- `R07_lower_left`
- `R08_lower_center`
- `R09_lower_right`

ROI 划分应依据实际烫钻密度和服装结构调整，不要求固定九宫格。

每个 ROI 必须：

- 独立裁切
- 至少进行一次高倍视觉检查
- 保留足够上下文以识别格纹周期
- 避免仅裁一颗亮点导致无法判断其与格纹关系

### 禁止

- 只看整张图做烫钻判断
- 用低分辨率预览代替局部放大
- 把所有亮点统一当作烫钻

---

## Stage 2 — Candidate Classification

### 目标
逐个区分：

- 水晶烫钻
- 格纹交点
- 黑色印花点
- 白色印花点
- 面料高光
- 无法判断的点

### 判定原则

不得仅凭“亮度”判断。

应综合：

- 形状
- 边界
- 凸起感
- 切面
- 反射方向
- 与格线的关系
- 与织纹的关系
- 周期规律
- 邻近区域是否出现相同辅料结构

### 强制规则

若一个点同时满足“格纹交点”与“可能是烫钻”的特征，但缺乏足够证据，则标记 `UNKNOWN`，禁止猜测。

---

## Stage 3 — Build Rhinestone Ledger

### 目标
在生成前建立一份烫钻身份账本，作为之后所有局部修复与 QC 的唯一依据之一。

### Ledger Minimum Fields

每个可确认烫钻至少记录：

```yaml
rhinestone:
  id: RH-R03-014
  region_id: R03
  classification: TRUE_RHINESTONE
  source_confidence: 0.98
  center_x_norm: 0.634
  center_y_norm: 0.281
  local_x_norm: 0.422
  local_y_norm: 0.617
  diameter_norm: 0.012
  shape: round_or_faceted
  material: clear_crystal_or_glass
  highlight_character: faceted_specular
  spacing_to_neighbors:
    nearest_left_norm: 0.081
    nearest_right_norm: 0.079
    nearest_up_norm: 0.124
    nearest_down_norm: 0.126
  notes: visible crystal edge and multi-face reflection
```

### 坐标规则

同时记录：

- 全图归一化坐标 `center_x_norm / center_y_norm`
- ROI 内局部坐标 `local_x_norm / local_y_norm`

这样即使服装整体尺寸发生轻微画布变化，也可通过 ROI 局部关系复核。

### 数量记录

每个 ROI 必须记录：

```yaml
region_summary:
  region_id: R03
  confirmed_rhinestones: 18
  unknown_candidates: 2
  plaid_intersections: 31
  black_print_dots: 0
  white_print_dots: 0
  fabric_highlights: 7
```

### 排列记录

除逐颗记录外，还应记录：

- 行列关系
- 平均横向间距
- 平均纵向间距
- 是否规则网格
- 是否错位排列
- 是否沿格纹特定单元分布
- 是否局部缺位属于原设计

禁止为了“更整齐”自动补全原本没有烫钻的位置。

---

## Stage 4 — Generate / Retouch the Locked Garment Base

### 目标
先得到一张商品身份稳定、不会因后续调整而反复漂移的服装底图。

### Base Lock 内容

底图阶段必须锁定：

- 颜色
- 面料类别
- 格纹比例
- 格纹方向
- 图案
- 结构
- 辅料
- 文字
- 蕾丝
- 刺绣
- 轮廓
- 原有烫钻分布的参考坐标系

### 关键原则

此阶段可以：

- 去背景
- 去污渍
- 去线头
- 轻度去褶皱
- 修复明显摄影瑕疵
- 整理轮廓

但只要操作会破坏烫钻坐标或覆盖烫钻区域，就必须降级处理或放弃。

### 关于烫钻

底图不得：

- 随机重绘烫钻
- 自动补钻
- 自动删钻
- 把暂时无法保留的烫钻变成白点

若底图生成后某烫钻区域不可靠，应将其标记为 `REPAIR_REQUIRED`，留给 Stage 5 局部修复，而不是重新生成整件衣服。

---

## Stage 5 — Local Rhinestone Second-Pass Repair

### 目标
对每个 `REPAIR_REQUIRED` ROI 做局部二次修复。

### 强制局部原则

只允许编辑当前错误 ROI 及必要的极小羽化边缘。

必须冻结：

- 其他 ROI
- 服装整体轮廓
- 已通过 QC 的格纹
- 已通过 QC 的烫钻
- 颜色
- 版型
- 文字
- 其他辅料

### 修复目标

逐个恢复：

- 烫钻数量
- 烫钻中心位置
- 烫钻大小
- 烫钻间距
- 水晶切面
- 微凸起体积
- 银白/透明高光
- 折射与反射
- 与布面的真实贴附关系

### 材质要求

烫钻应表现为真实小型水晶/玻璃辅料：

- 透明或半透明晶体
- 有多面切面
- 有小范围高亮反射
- 有局部暗切面
- 有真实边缘
- 有微小高度
- 不得变成纯白实心圆点

---

## Stage 6 — Magnified Region-by-Region QA

### 目标
输出后不看整图“感觉差不多”，而是重新放大每一个 ROI，与原图逐区域比对。

### 每个 ROI 必检

1. **Count Check**
   - 数量是否完全一致
   - 是否新增
   - 是否丢失

2. **Position Check**
   - 是否移动
   - 是否因去褶皱而整体漂移
   - 是否被吸附到格纹交点

3. **Spacing Check**
   - 横向间距
   - 纵向间距
   - 邻近关系

4. **Size Check**
   - 是否被放大
   - 是否被缩小
   - 是否不同区域尺寸不一致

5. **Material Check**
   - 是否仍是水晶
   - 是否变成白点
   - 是否变成黑点
   - 是否变成亮片
   - 是否变成普通高光

6. **Layer Check**
   - 是否仍位于面料表面
   - 是否被融合进面料纹理

7. **Plaid Integrity Check**
   - 修钻时是否破坏格纹线
   - 是否产生格纹扭曲
   - 是否出现第三种颜色

### Position Tolerance

在原图足够清晰时，要求视觉位置与原图严格匹配。

若需数值化 QC：

- 单颗中心位移超过该颗烫钻直径的 `0.25×` → FAIL
- 明显跨越格纹单元或吸附到相邻格纹交点 → FAIL
- 可见数量差异 `!= 0` → FAIL

---

## Stage 7 — Region-Only Retry Loop

### 目标
任何未通过 QC 的区域只重做该区域。

### 强制规则

当底图已通过结构与颜色检查后：

> **禁止因为一个局部烫钻错误而重新生成整件衣服。**

失败处理：

```text
ROI FAIL
→ 冻结整张已通过底图
→ 锁定所有已通过 ROI
→ 只定位失败 ROI
→ 读取该 ROI 的 Rhinestone Ledger
→ 仅重做错误点/错误小区域
→ 再次 Stage 6 QA
```

### Retry Causes

以下任一情况触发局部重做：

- 少 1 颗或以上
- 多 1 颗或以上
- 位置明显移动
- 间距改变
- 尺寸明显改变
- 水晶变白点
- 水晶变黑点
- 水晶变亮片
- 水晶切面丢失
- 修复造成格纹破坏

---

## Stage 8 — Final Full-Garment Verification

只有所有 ROI 均通过后，才做最后整图检查。

最终检查：

- 所有 ROI 状态 = PASS
- 总烫钻数量与账本一致
- 无烫钻跨 ROI 重复生成
- 无边缘 ROI 漏检
- 无白点伪装成烫钻
- 无格纹交点被错误晶体化
- 无随机新增闪点
- 颜色保持
- 格纹保持
- 面料保持
- 结构保持
- 版型优化没有覆盖烫钻

---

# QC Status Model

每个区域只能使用以下状态：

```yaml
status:
  - PASS
  - REPAIR_REQUIRED
  - UNKNOWN_REFERENCE_REQUIRED
```

### PASS
所有可见烫钻数量、位置、大小、材质和间距通过。

### REPAIR_REQUIRED
原图足够清楚，但输出有局部错误，可继续局部修复。

### UNKNOWN_REFERENCE_REQUIRED
原图不足以确认真实信息。必须停止并要求补图。

禁止用“看起来差不多”“基本一致”替代 QC 状态。

---

# Region Repair Instruction Template

对失败区域使用如下逻辑：

```text
只编辑 ROI {region_id}。
冻结 ROI 外所有像素级视觉内容与商品结构。
以原图该 ROI 和 Rhinestone Ledger 为唯一位置/数量依据。
恢复确认的 {confirmed_count} 颗真实水晶烫钻。
禁止新增、删除、移动、复制或合并烫钻。
禁止将水晶烫钻画成纯白点、黑点、印花点、亮片或面料高光。
每颗烫钻必须保持独立立体辅料属性：微凸起、水晶/玻璃切面、真实高光与折射、贴附在布面表层。
保持该 ROI 原格纹线宽、间距、方向和颜色不变。
禁止修改其他已通过区域。
```

---

# Special Rules for Plaid + Rhinestone Garments

格纹是烫钻误判最高发的面料之一，必须追加以下限制。

## Plaid Grid Lock

先识别：

- 横向格线
- 纵向格线
- 格纹重复周期
- 黑白/粉棕等颜色单元
- 格纹交点坐标

然后将格纹交点作为一个独立候选集合，与烫钻集合分离。

### 禁止

- 把格纹交点当烫钻
- 为了保留烫钻而把格纹交点全部变亮
- 修钻时抹断格线
- 修钻时拉伸格子
- 让烫钻自动吸附到最近格纹交点

---

# Rules for User-Provided Material Reference

如果用户提供第二张图仅作为“烫钻材质参考”：

### 图 1 / 主参考
负责：

- 数量
- 位置
- 间距
- 排列规律
- 尺寸关系
- 哪些区域有钻 / 无钻

### 图 2 / 材质参考
只负责：

- 水晶透明度
- 切面
- 反射
- 折射
- 高光形态
- 立体颗粒感

### 强制规则

不得把材质参考图中的：

- 数量
- 密度
- 排列方式
- 坐标

迁移到主图。

---

# No-Rhinestone Zones

若用户明确指出某些纯色区域、灰色区域、里布区域或其他区域 **没有烫钻**，应建立 `NO_RHINESTONE_MASK`。

这些区域：

- 禁止新增烫钻
- 禁止新增随机亮点
- 禁止复制相邻格纹区的烫钻

---

# Interaction Rules

## 当参考足够清楚

直接执行完整流程，不需要让用户反复确认。

## 当参考不足

不要继续生成一个“可能正确”的版本。

应明确指出：

- 哪个 ROI 看不清
- 哪些候选点无法分类
- 需要补充什么角度/清晰度的微距图

---

# Failure Modes — Zero Tolerance

以下情况视为失败：

- 任意确认烫钻丢失
- 任意确认烫钻无依据新增
- 烫钻变成纯白点
- 烫钻变成黑点
- 烫钻变成平面印花
- 烫钻变成随机闪光噪点
- 烫钻材质变塑料珠
- 烫钻被磨皮
- 烫钻被褶皱修复覆盖
- 烫钻被版型拉伸移动
- 烫钻被对称化算法重排
- 烫钻数量为了“看起来均匀”被修改
- 格纹交点被错误晶体化
- 水晶被错误并入面料纹理层
- 为修一个局部错误重新生成整件已通过底图
- 原图看不清却继续猜测数量或位置

---

# Default Execution Policy

```yaml
rhinestone_preservation:
  rhinestone_layer_type: independent_3d_accessory
  priority: highest_detail_priority
  preserve_before_dewrinkle: true
  preserve_before_symmetry: true
  preserve_before_beautification: true
  crop_and_magnify_first: true
  classify_candidates: true
  build_ledger_before_generation: true
  use_global_and_local_normalized_coordinates: true
  lock_base_before_local_repair: true
  local_second_pass_required: true
  region_by_region_qc: true
  retry_scope: failed_region_only
  whole_garment_regeneration_after_base_pass: forbidden
  hallucination_when_unclear: forbidden
  request_macro_reference_when_unclear: required
```

---

# Execution Summary

调用 `$rhinestone-preservation` 时，必须遵循：

```text
1. 检查原图清晰度
2. 找出所有烫钻候选区域
3. 单独裁切并放大每个 ROI
4. 区分水晶烫钻 / 格纹交点 / 黑白印花点 / 面料高光 / UNKNOWN
5. 建立 Rhinestone Ledger：数量、坐标、间距、大小、材质、置信度
6. 锁定服装底图，禁止因美化破坏烫钻坐标系
7. 对 REPAIR_REQUIRED 区域做局部二次修复
8. 放大逐 ROI 对比原图与输出
9. 检查丢失、移动、增钻、缩放、变白点、变黑点、变亮片、格纹破坏
10. 未通过 → 只重做失败区域，不重新生成整件衣服
11. 全部 ROI PASS 后才输出最终图
12. 原图无法确认 → 停止猜测，要求高清烫钻微距参考图
```

**最高原则：烫钻是独立立体辅料层。对带烫钻商品而言，正确保留烫钻的优先级高于去褶皱、版型对称和整体美化。**
