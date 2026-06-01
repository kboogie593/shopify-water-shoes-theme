# FurQuiet 1688 Supplier Message

Updated: 2026-06-01

Use this message when contacting 1688 suppliers for the pet grooming vacuum sample. The goal is to verify sample access, launch-market readiness, replacement filters, packaging, and media rights before opening serious checkout volume.

## Initial Message

你好，我们准备采购宠物美容吸毛器/宠物美容吸尘器套装，目标市场是美国、加拿大、英国、澳大利亚。现在先采购样品做测试，通过后再评估首批订单。

请帮忙确认以下信息：

1. 是否支持购买 1-3 台样品？样品价格和国内运费是多少？
2. 套装具体包含哪些配件？请列出主机、软管、梳头、推剪、限位梳、吸嘴、滤芯、清洁刷、收纳底座等明细。
3. 是否有美规/英规/澳规插头？电压标签是否支持对应市场？
4. 是否有 CE、FCC、UKCA、UL、ETL 或其他检测/认证资料？如果有请发图片或文件。
5. 滤芯、梳头、软管是否可以单独补货？补货 MOQ 和单价是多少？
6. 是否有英文说明书和英文包装？可以发说明书、标签、包装盒照片吗？
7. 外箱尺寸、单台重量、装箱重量分别是多少？
8. 噪音分贝是否有测试数据？如果有请提供测试距离和档位。
9. 我们是否可以临时使用你们提供的无水印产品图片做测试页面？后续我们会用自己拍摄的样品图替换。
10. 样品发出时间和量产交期分别是多少？

如果可以，请同时发一段实际开机视频、配件展示视频、包装视频。谢谢。

## Reply Scoring

Score each supplier in `data/furquiet-supplier-scorecard.csv`:

- `Sample Available`: yes/no and sample quote.
- `Plug Options`: US/UK/AU support.
- `Voltage Label`: whether launch-market labels match.
- `Cert Docs`: whether documents are real and readable.
- `Replacement Filters`: whether consumables can be reordered.
- `English Manual`: whether customer-facing instructions are ready.
- `Packaging Dimensions`: required for shipping math.
- `Media Permission`: must avoid watermarked or competitor media.
- `Lead Time Days`: sample and first-batch timing.

Reject suppliers that cannot provide samples, replacement filters, clear labels, or basic packaging dimensions.
