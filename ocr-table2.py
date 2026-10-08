#!/usr/local/bin/python3
import os
import cv2
from paddleocr import PPStructure, draw_structure_result, save_structure_res

table_engine = PPStructure(show_log=True)

save_folder = 'path/to/output/'  # folder for the results
if not os.path.exists(save_folder):
    os.mkdir(save_folder)

img_path = 'path/to/table.png'  # path to your picture
img = cv2.imread(img_path)
result = table_engine(img)
print(result)

save_structure_res(result, save_folder, os.path.basename(img_path + ".xlsx"))
