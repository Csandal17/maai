"""
test_chinese_pdf.py — proves the PDF renders non-Latin scripts.

Runs the full pipeline (intake -> normalise -> PDF) on the Chinese
description, including the untranslatable 上火 expression. If her
characters render correctly in the PDF, the equity hook survives
all the way to the physical document.
"""

from chain import build_record
from make_pdf import make_pdf

description_zh = (
    "我晚上总是睡不好，半夜会突然发热、出一身汗。"
    "白天特别累，没什么精神，注意力也集中不了。"
    "月经也乱七八糟的。而且我总感觉自己很上火，心里很烦躁。"
)

record = build_record(description_zh, language="zh")
path = make_pdf(record, output_path="maai_record_zh.pdf")
print(f"\nChinese PDF written: {path}")

