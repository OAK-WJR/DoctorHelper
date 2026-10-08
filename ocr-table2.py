#!/usr/bin/env python3
"""Experiment: turn a picture of a table into an Excel file with PaddleOCR's table recognition (PP-Structure)."""
# The PP-Structure calls are adapted, with changes, from the quick-start example in PaddleOCR's documentation
# (Copyright (c) 2016 PaddlePaddle Authors, Apache License 2.0; see THIRD_PARTY_NOTICES.md).
import argparse, os
import cv2
from paddleocr import PPStructure, save_structure_res

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("image", help="picture of a table")
parser.add_argument("output", help="folder to save the results in")
args = parser.parse_args()

img = cv2.imread(args.image)
if img is None:
  parser.error(f"cannot read {args.image}")

os.makedirs(args.output, exist_ok=True)
table_engine = PPStructure(show_log=True)
result = table_engine(img)

save_structure_res(result, args.output, os.path.splitext(os.path.basename(args.image))[0])
print("saved to", args.output)
