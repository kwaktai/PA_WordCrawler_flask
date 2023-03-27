

# https://jehyunlee.github.io/2023/02/20/Python-DS-128-transqual/

import requests
import json


def translate_text(text, source_lang, target_lang):
    url = "https://deepl-translator.p.rapidapi.com/translate"
    payload = {
        "text": text,
        "source": source_lang,
        "target": target_lang
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "daa51937a2mshf2bc3aefe562b9cp156d26jsn7902e400041e",
        "X-RapidAPI-Host": "deepl-translator.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    result = json.loads(response.text)

    if "translations" in result:
        translated_text = result["translations"][0]["text"]
    else:
        translated_text = ""

    return translated_text


print(translate_text("In the example below, we first let it complete our explanation, and then, line by line, we tab through the code that does what we just said in English.", "EN", "KO"))
