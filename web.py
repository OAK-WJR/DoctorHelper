#!/usr/bin/env python3
"""Doctor-Helper demo: read photos of a Chinese medical record, translate the text into English and summarize it.

The page translates in the browser, with Chrome's built-in Translator API, so the server only reads photos and summarizes.
"""
import os, tempfile
from flask import Flask, render_template, request, jsonify, redirect, url_for
from paddleocr import PaddleOCR
import summarizer

PICTURE_TYPES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB per request

ocr = PaddleOCR(lang="ch")

@app.route('/')
def index():
  return redirect(url_for('main_page'))

@app.route('/main')
def main_page():
  return render_template('main.html')

@app.route('/recognize', methods=['POST'])
def recognize_text():
  images = [image for image in request.files.getlist('image') if image.filename]
  if not images:
    return jsonify({"error": "Please choose at least one photo."}), 400

  all_texts = []
  for image in images:
    suffix = os.path.splitext(image.filename)[1].lower()
    # The photo is only kept in a temporary folder that is deleted right after reading
    with tempfile.TemporaryDirectory() as folder:
      path = os.path.join(folder, "photo" + (suffix if suffix in PICTURE_TYPES else ".png"))
      image.save(path)
      results = ocr.ocr(path)
    lines = results[0] if results and results[0] else []
    all_texts.append("\n".join(line[1][0] for line in lines))

  return jsonify({"recognized_text": "\n\n".join(all_texts).strip()})

@app.errorhandler(413)
def too_large(error):
  return jsonify({"error": "The photos are too large (20 MB in total at most)."}), 413

@app.route('/summarize', methods=['POST'])
def summarize_text():
  return jsonify({"summary": summarizer.run(request.form.get('text', ''))})

if __name__ == '__main__':
  # Only this computer can open the page, and the Flask debugger stays off
  app.run(host='127.0.0.1', port=8000, debug=False)
