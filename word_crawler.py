import os
import csv
from collections import Counter
from googletrans import Translator
from typing import List, Tuple
from tkinter import messagebox


def translate_text(text: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, int]]]:
    # 번역기 객체를 생성합니다.
    translator = Translator()

    # 영어 문장과 번역된 한국어 문장을 저장할 리스트를 생성합니다.
    translated_sentences = []

    # 영어 단어와 출현 빈도를 저장할 Counter 객체를 생성합니다.
    word_counter = Counter()

    # 영어 문장과 번역된 한국어 문장을 저장합니다.
    for sentence in text.split("."):
        if sentence.strip():
            translated_sentence = translator.translate(
                sentence, src="en", dest="ko").text
            translated_sentences.append(
                (sentence.strip(), translated_sentence))

            # 영어 단어와 출현 빈도를 세어 저장합니다.
            words = [word.lower()
                     for word in sentence.split() if word.isalpha()]
            word_counter.update(words)

    # 출현 빈도가 가장 높은 상위 20개 단어를 추출합니다.
    top_words = word_counter.most_common(20)

    # 번역된 단어를 저장할 리스트를 생성합니다.
    translated_words = []

    # 영어 단어와 번역된 한국어 단어를 저장합니다.
    for word in top_words:
        translated_word = translate_word(word[0]).strip()
        translated_words.append((word[0], translated_word))
    print(translated_words)

    return translated_sentences, translated_words


def translate_word(word: str) -> str:
    # 번역기 객체를 생성합니다.
    translator = Translator()

    # 단어를 번역합니다.
    translated_word = translator.translate(word, src="en", dest="ko").text
    print(translated_word)
    return translated_word


DATA_DIR = "data"
WORDS_FILENAME = "words.csv"
SENTENCES_FILENAME = "sentences.csv"
WORDS_DATA_FILENAME = "words_data.csv"
SENTENCES_DATA_FILENAME = "sentences_data.csv"


def save_data(table):

    words_table = {k: v for k, v in table.items() if k.startswith(
        '영어 단어') or k.startswith('번역된 한국어 단어')}
    sentences_table = {k: v for k, v in table.items() if k.startswith(
        '영어 문장') or k.startswith('번역된 한국어 문장')}

    save_individual_data(words_table, WORDS_FILENAME)
    save_individual_data(sentences_table, SENTENCES_FILENAME)

    save_cumulative_data(words_table, WORDS_DATA_FILENAME)
    save_cumulative_data(sentences_table, SENTENCES_DATA_FILENAME)


def save_individual_data(table, filename):
    filepath = os.path.join(DATA_DIR, filename)

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(table.keys())
        writer.writerows(zip(*table.values()))

    print(f"{filename}에 새로운 데이터가 저장되었습니다.")


def save_cumulative_data(table, filename):
    filepath = os.path.join(DATA_DIR, filename)

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    existing_data = []
    if os.path.exists(filepath):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            try:
                header = next(reader)
            except StopIteration:
                header = None

            if header:
                for row in reader:
                    existing_data.append(row)

    new_data = list(zip(*table.values()))

    # 중복 단어 제거 로직
    existing_data_dict = {}
    for row in existing_data:
        english_word, translated_word = row
        if english_word not in existing_data_dict:
            existing_data_dict[english_word] = set()
        existing_data_dict[english_word].add(translated_word)

    filtered_data = []
    for row in new_data:
        english_word, translated_word = row
        if len(english_word) > 1 and (english_word not in existing_data_dict or translated_word not in existing_data_dict[english_word]):
            filtered_data.append(row)
            if english_word not in existing_data_dict:
                existing_data_dict[english_word] = set()
            existing_data_dict[english_word].add(translated_word)

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if header:
            writer.writerow(header)
        else:
            writer.writerow(table.keys())

        # 기존 데이터와 새로운 데이터를 결합합니다.
        combined_data = existing_data + filtered_data

        # 모든 데이터의 길이가 같아지도록 공백을 추가합니다.
        max_length = max([len(row) for row in combined_data])
        for i, row in enumerate(combined_data):
            if len(row) < max_length:
                combined_data[i] += [''] * (max_length - len(row))

        writer.writerows(combined_data)

    print(f"{filename}에 기존 데이터가 보존되고 새로운 데이터가 추가되었습니다.")


# translate_text(
#     "Hello, world. I am a student. I am studying English. I am studying Python. I am studying Englis")

if __name__ == "__main__":
    text = "Hello, world. I am a student. I am studying English. I am studying Python. I am studying Englis"
    translated_sentences, translated_words = translate_text(text)
    # 데이터를 저장합니다.
    save_data({
        '영어 문장': [x[0] for x in translated_sentences],
        '번역된 한국어 문장': [x[1] for x in translated_sentences],
        '영어 단어': [x[0] for x in translated_words],
        '번역된 한국어 단어': [x[1] for x in translated_words],
    })

    # 저장된 데이터를 출력합니다.
    with open(os.path.join(DATA_DIR, SENTENCES_DATA_FILENAME), newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)

    with open(os.path.join(DATA_DIR, WORDS_DATA_FILENAME), newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)
