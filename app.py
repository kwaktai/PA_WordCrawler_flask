import os
import csv
from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from typing import List, Tuple
from collections import Counter


app = Flask(__name__)

DATA_DIR = "data"
WORDS_FILENAME = "words.csv"
SENTENCES_FILENAME = "sentences.csv"
WORDS_DATA_FILENAME = "words_data.csv"
SENTENCES_DATA_FILENAME = "sentences_data.csv"


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

    with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(zip(*table.values()))

    print(f"{filename}에 새로운 데이터가 저장되었습니다.")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    text = request.json['text']
    # text = "One difference between worry about AI and worry about other kinds of technologies (e.g. nuclear power, vaccines) is that people who understand it well worry more, on average, than people who don't. That difference is worth paying attention to."
    translated_sentences, translated_words = translate_text(text)
    save_data({
        '영어 문장': [x[0] for x in translated_sentences],
        '번역된 한국어 문장': [x[1] for x in translated_sentences],
        '영어 단어': [x[0] for x in translated_words],
        '번역된 한국어 단어': [x[1] for x in translated_words],
    })
    return jsonify({
        'translated_sentences': translated_sentences,
        'translated_words': translated_words
    })


@app.route("/save", methods=["POST"])
def save():
    table = request.form.to_dict()
    save_data(table)
    return render_template("save.html")


if __name__ == "__main__":
    app.run(debug=True)
