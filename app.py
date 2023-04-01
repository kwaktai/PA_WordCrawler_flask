from flask import Flask, request, jsonify, render_template
from googletrans import LANGUAGES
from word_crawler import translate_text, save_data

app = Flask(__name__)


@app.route("/")
def index():
    print("index_TEST")
    return render_template('index.html', languages=LANGUAGES)


@app.route("/translate", methods=["POST"])
def translate():
    print("translate_TEST")
    text = request.json["text"]
    # text = request.get_json()["text"]
    # text = "The Tesla Model Y became the best-selling Danish vehicle in a month of all time:"
    translated_sentences, translated_words = translate_text(text)

    # 데이터를 저장합니다.
    save_data({
        '영어 문장': [x[0] for x in translated_sentences],
        '번역된 문장': [x[1] for x in translated_sentences],
        '영어 단어': [x[0] for x in translated_words],
        '번역된 단어': [x[1] for x in translated_words],
    })

    # 번역 결과를 반환합니다.
    return jsonify({
        "sentences": [x[1] for x in translated_sentences],
        "words": [x[1] for x in translated_words]
    })


if __name__ == "__main__":
    app.run(debug=True)
