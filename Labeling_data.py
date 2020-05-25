import numpy as np
import cv2
import os
import shutil

# was too slow would label data one by one

class LabelData:
    def __init__(self, path_input, output_path, list_input_path=None):
        self.path_input = path_input
        self.list_input_path = list_input_path
        self.output_path = output_path
        self.key_path_dict = {49: "Label 1", 50: "Label 2", 51: "Label 3"}

    def label_picture(self, img_path):
        tot_path = f"{self.path_input}/{img_path}"
        img = cv2.imread(tot_path, 1)
        cv2.imshow('image', img)
        c = cv2.waitKey(0)
        self._compare_key(c, img_path)
        cv2.destroyAllWindows()

    def label_all_pictures(self):
        img_path_list = os.listdir(self.path_input)
        for img_path in img_path_list:
            self.label_picture(img_path)

    def _compare_key(self, keypress: int, img_path):
            if keypress in self.key_path_dict:
                print(keypress)
                self._move_dir(img_path, keypress)

    def _move_dir(self, img_path, keypress):
        input_path = f"{self.path_input}/{img_path}"
        output_path = f"{self.output_path}/{self.key_path_dict[keypress]}/{img_path}"
        shutil.move(input_path, output_path)






