import clipboard
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
# from deepl import translate_text
from googletrans import Translator
import pandas as pd

# 웹사이트에서 데이터를 크롤링하는 함수


def get_text_from_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.get_text()

# 텍스트에서 영어 단어를 추출하는 함수


def extract_words(text):
    words = re.findall(r'\b\w+\b', text)
    return [word.lower() for word in words if word.isalpha()]


# 전역 테이블 변수를 초기화합니다.
table = {
    "영어 문장": [],
    "번역된 한국어 문장": [],
    "영어 단어": [],
    "번역된 한국어 단어": []
}

_original_text = ""


def process_text(input_text):
    global _original_text
    _original_text = input_text

    text = input_text

    # 텍스트에서 영어 단어를 추출합니다.
    words = extract_words(text)

    # 단어의 빈도를 계산합니다.
    word_freq = Counter(words)

    # 자주 등장하는 단어를 추출합니다.
    top_words = word_freq.most_common(10)

    # Google 번역 API를 사용합니다.
    translator = Translator()

    # 영어 문장과 번역된 한국어 문장을 저장합니다.
    for sentence in text.split("."):
        if sentence.strip():
            table["영어 문장"].append(sentence.strip())
            table["번역된 한국어 문장"].append(translator.translate(
                sentence, src="en", dest="ko").text)

    # 영어 단어와 번역된 한국어 단어를 저장합니다.
    for word in top_words:
        table["영어 단어"].append(word[0])
        table["번역된 한국어 단어"].append(translator.translate(
            word[0], src="en", dest="ko").text)

    # for sentence in text.split("."):
    #     if sentence.strip():
    #         table["영어 문장"].append(sentence.strip())
    #         translated_text = translate_text(sentence.strip(), "EN", "KO")
    #         table["번역된 한국어 문장"].append(translated_text)

    # # 영어 단어와 번역된 한국어 단어를 저장합니다.
    # for word in top_words:
    #     table["영어 단어"].append(word[0])
    #     translated_word = translate_text(word[0], "EN", "KO")
    #     table["번역된 한국어 단어"].append(translated_word)

    # 결과를 출력합니다.
    for key, value in table.items():
        print(f"{key}: {value}")


def get_table():
    return table


def get_original_text():
    return _original_text


def save_to_csv():
    global table
    csv_file = "output.csv"

    # DataFrame을 생성하고, 테이블의 데이터를 추가합니다.
    df = pd.DataFrame(table)

    # 기존 CSV 파일이 있는 경우, 데이터를 읽어옵니다.
    try:
        existing_data = pd.read_csv(csv_file)
        # 새로운 데이터를 기존 데이터와 결합합니다.
        combined_data = pd.concat([existing_data, df])
    except FileNotFoundError:
        # 기존 파일이 없는 경우, 새로운 데이터만 저장합니다.
        combined_data = df

    # 결합된 데이터를 CSV 파일에 저장합니다.
    combined_data.to_csv(csv_file, index=False)
