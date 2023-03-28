from flask import Flask, render_template, request, jsonify

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


if __name__ == '__main__':
    app.run(debug=True)
