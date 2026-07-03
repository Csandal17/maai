"""
test_chinese.py — stress-tests Maai's equity hook on a non-Latin script.

Runs a Chinese symptom description through intake() then normalise(),
including one culturally-specific expression ("上火") that has no clean
Western clinical equivalent — to see whether Maai preserves her exact
characters and stays honest where a tidy mapping doesn't exist.
"""

from intake import intake
from normalise import normalise

# A Mandarin-speaking patient, similar symptom cluster, plus one
# Traditional-Chinese-Medicine expression ("上火") with no direct clinical term.
description_zh = (
    "我晚上总是睡不好，半夜会突然发热、出一身汗。"
    "白天特别累，没什么精神，注意力也集中不了。"
    "月经也乱七八糟的。而且我总感觉自己很上火，心里很烦躁。"
)

record = intake(description_zh, language="zh")
result = normalise(record["verbatim_description"])

print(f"\nDETECTED LANGUAGE: {result['detected_language']}")
print("\nHER WORDS (original language)  →  CLINICAL TERMS (English)\n")
for item in result["items"]:
    print(f'  "{item["verbatim"]}"')
    print(f'   → {item["clinical"]}\n')
    