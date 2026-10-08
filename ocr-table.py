#!/usr/local/bin/python3
import os
from paddleocr import PaddleOCR
from PIL import Image
from pprint import pprint

def ocr(folder_path):
  ocr = PaddleOCR(lang="ch")
  images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf'))]

  results = []
  for image in images:
    results.append(ocr.ocr(image))
  
  return results

def get_reference_y(rect):
  return (rect[0][1] + rect[2][1]) / 2

def group_line_v2(data, threshold=10):
  blocks = data[0]
  
  blocks.sort(key=lambda block: get_reference_y(block[0]))

  rows = []
  current_row = [blocks[0]]

  for i in range(1, len(blocks)):
    if abs(get_reference_y(blocks[i][0]) - get_reference_y(current_row[-1][0])) < threshold:
      current_row.append(blocks[i])
    else:
      rows.append(current_row)
      current_row = [blocks[i]]

  if current_row:
    rows.append(current_row)
      
  for row in rows:
    row.sort(key=lambda box: box[0][0])
  
  return rows

data = ocr("path/to/scans/")

grouped_data = []
for single_page_data in data:
  grouped_data.append(group_line_v2(single_page_data))

for single_page_data in grouped_data:
  for i, row in enumerate(single_page_data):
    print(f"Row {i + 1}:")
    for box in row:
      print(box[1][0])
    print("\n")