from flask import Flask, render_template, request, jsonify
import word_crawler_clipboard

app = Flask(__name__)

stored_words = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/store_words', methods=['POST'])
def store_words():
    words = request.json['words']
    for word in words:
        if word not in stored_words:
            stored_words.append(word)
    return jsonify(stored_words)


@app.route('/process_text', methods=['POST'])
def process_text():
    input_text = request.json['input_text']
    word_crawler_clipboard.process_text(input_text)
    table = word_crawler_clipboard.get_table()
    word_crawler_clipboard.save_to_csv()
    return jsonify(table)


if __name__ == '__main__':
    app.run(debug=True)
