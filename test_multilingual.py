"""
test_multilingual.py — proves Maai's equity hook.

Runs a non-English symptom description through intake() then normalise(),
showing her original words preserved in her language, with English clinical
terms alongside for the clinician. This is the whole reason Maai exists.
"""

from intake import intake
from normalise import normalise

# A Spanish-speaking patient describing the same symptom cluster in her own words
description_es = (
    "Me despierto a las 3 de la madrugada empapada en sudor, y durante el día "
    "estoy tan agotada que no me puedo concentrar. Además mi regla está muy irregular."
)

record = intake(description_es, language="es")
result = normalise(record["verbatim_description"])

print("\nHER WORDS (original language)  →  CLINICAL TERMS (English)\n")
for item in result["items"]:
    print(f'  "{item["verbatim"]}"')
    print(f'   → {item["clinical"]}\n')
    