import os
import csv


# 저장할 폴더를 확인하고 없으면 생성합니다.

def save_data(table):
    output_folder = "data"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 영어 문장과 번역된 한국어 문장을 저장합니다.
    with open(os.path.join(output_folder, "sentences.csv"), "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["영어 문장", "번역된 한국어 문장"])

        for en_sentence, ko_sentence in zip(table["영어 문장"], table["번역된 한국어 문장"]):
            writer.writerow([en_sentence, ko_sentence])

    # 영어 단어와 번역된 한국어 단어를 저장합니다.
    with open(os.path.join(output_folder, "words.csv"), "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["영어 단어", "번역된 한국어 단어"])

        for en_word, ko_word in zip(table["영어 단어"], table["번역된 한국어 단어"]):
            writer.writerow([en_word, ko_word])

    print("테이블 데이터가 data 폴더에 저장되었습니다.")

def main():
    pass

if __name__ == "__main__":
    main()
