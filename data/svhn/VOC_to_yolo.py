# darknet/voc_label.py
import os
import xml.etree.ElementTree as ET


def convert(size, box):
    print(size, box)
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    # print(image_id)
    in_file = open('data/svhn/Annotations/{}'.format(image_id), 'rb')

    out_file = open('data/svhn/trainval/{}'.format(
                    image_id.replace('.xml', '.txt')), 'w')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls == "10":  # 10 to 0 digit
            cls = "0"
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls) + " " + " ".join([str(a) for a in bb]) + '\n')


if __name__ == "__main__":
    image_ids_train = os.listdir("data/svhn/Annotations")
    # os.makedirs('data/svhn/labels/', exist_ok=True)

    for image_id in image_ids_train:
        # print(image_id)
        convert_annotation(image_id)

    print("DONE.")
