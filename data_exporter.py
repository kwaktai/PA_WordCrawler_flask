import csv
import os

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
