#!/usr/local/bin/python3

import test
from flask import Flask, render_template, request, jsonify, redirect, url_for
from paddleocr import PaddleOCR
from transformers import T5ForConditionalGeneration, T5Tokenizer

app = Flask(__name__)

ocr = PaddleOCR(lang="ch")
MODEL_NAME = 't5-small'
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

@app.route('/')
def index():
    return redirect(url_for('main_page'))

@app.route('/main')
def main_page():
    return render_template('main.html')

@app.route('/recognize', methods=['POST'])
def recognize_text():
    image = request.files['image']
    if image:
        image.save("uploaded_image.jpg")
        results = ocr.ocr("uploaded_image.jpg")
        recognized_text = "\n".join(txt[1][0] for txt in results[0])
        print(recognized_text)
        return jsonify({"recognized_text": recognized_text})

@app.route('/translate', methods=['POST'])
def translate_text():
    text = request.form['text']
    translated_text = ""   # not included in this public copy
    print(translated_text)
    return jsonify({"translated_text": translated_text})

@app.route('/summarize', methods=['POST'])
def summarize_text():
    text = request.form['text']
    summary = test.run(text)
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)
