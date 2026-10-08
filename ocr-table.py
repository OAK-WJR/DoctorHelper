#!/usr/bin/env python3
"""Experiment: read table-like reports with PaddleOCR and print the text row by row."""
import argparse, os
from paddleocr import PaddleOCR

def ocr(folder_path):
  engine = PaddleOCR(lang="ch")
  images = [os.path.join(folder_path, f) for f in sorted(os.listdir(folder_path))
            if not f.startswith(".") and f.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf'))]
  return [engine.ocr(image) for image in images]

def get_reference_y(rect):
  return (rect[0][1] + rect[2][1]) / 2

def group_line_v2(data, threshold=10):
  """Put text boxes whose middles are less than threshold pixels apart into the same row."""
  blocks = data[0] if data and data[0] else []
  if not blocks:
    return []

  blocks.sort(key=lambda block: get_reference_y(block[0]))

  rows = []
  current_row = [blocks[0]]

  for i in range(1, len(blocks)):
    if abs(get_reference_y(blocks[i][0]) - get_reference_y(current_row[-1][0])) < threshold:
      current_row.append(blocks[i])
    else:
      rows.append(current_row)
      current_row = [blocks[i]]

  rows.append(current_row)

  for row in rows:
    row.sort(key=lambda box: box[0][0])

  return rows

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("folder", help="folder with the report pictures")
  args = parser.parse_args()

  for single_page_data in ocr(args.folder):
    for i, row in enumerate(group_line_v2(single_page_data)):
      print(f"Row {i + 1}:")
      for box in row:
        print(box[1][0])
      print("\n")
