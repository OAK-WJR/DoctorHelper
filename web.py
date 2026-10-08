#!/usr/local/bin/python3

import test
import os
from werkzeug.utils import secure_filename
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
  images = request.files.getlist('image')
  all_texts = []

  for image in images:
    filename = secure_filename(image.filename)
    image_path = os.path.join("uploads", filename)
    image.save(image_path)
    results = ocr.ocr(image_path)
    recognized_text = "\n".join(txt[1][0] for txt in results[0])
    all_texts.append(recognized_text)
    
  combined_text = "\n\n".join(all_texts)
  print(combined_text)
  return jsonify({"recognized_text": combined_text})

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
  app.run(host='0.0.0.0', port=80, debug=True)
