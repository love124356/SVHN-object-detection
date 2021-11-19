import os
import cv2
from tqdm import tqdm
import json
import argparse


def infer(opt):
    prediction = []
    txt_dir = os.listdir(opt.txt)
    # Read image (Be careful with the image order)
    # print(len(txt_dir))
    txt_dir.sort(key=lambda x: int(x[:-4]))
    for txt_name in tqdm(txt_dir):
        img_name = txt_name.replace(".txt", ".png")
        img_path = os.path.join(opt.data, img_name)
        img = cv2.imread(img_path)
        h, w, c = img.shape

        txt_path = os.path.join(opt.txt, txt_name)
        f = open(txt_path, 'r')
        contents = f.readlines()
        for content in contents:
            ans = {}
            content = content.strip().split(' ')
            ans['image_id'] = int(img_name.split(".")[0])
            ans['score'] = float(content[5])
            ans["category_id"] = int(content[0])
            w_center = w*float(content[1])
            h_center = h*float(content[2])
            width = w*float(content[3])
            height = h*float(content[4])
            left = float(w_center - width/2.0)
            right = float(w_center + width/2.0)
            top = float(h_center - height/2.0)
            bottom = float(h_center + height/2.0)
            ans['bbox'] = [left, top, right-left, bottom-top]

            prediction.append(ans)
        f.close()
    json_object = json.dumps(prediction, indent=4)
    with open("answer.json", "w") as outfile:
        outfile.write(json_object)
    print("DONE. answer.json is saved in root.")


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--txt', type=str, default='runs/detect/exp/labels/',
                        help='training labels txt path')
    parser.add_argument('--data', type=str, default='data/svhn/test/',
                        help='testing data path')

    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    infer(opt)
