import matplotlib.image as image
import json
import os

headstr = """\
<annotation>
    <folder>VOC2007</folder>
    <filename>%s</filename>
    <source>
        <database>The VOC2007 Database</database>
        <annotation>PASCAL VOC2007</annotation>
        <image>flickr</image>
        <flickrid>220208496</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>company</name>
    </owner>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""
objstr = """\
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
"""

tailstr = '''\
</annotation>
'''
if __name__ == "__main__":
    json_path = "data/svhn/MatTransform.json"
    with open(json_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    print("Make folder Annotations")
    os.makedirs('data/svhn/Annotations/', exist_ok=True)
    # os.makedirs('data/svhn/trainval/', exist_ok=True)

    dir = 'data/svhn/trainval/'
    for i in data:
        # print(i)
        img = image.imread(dir + i)
        head = headstr % (i, img.shape[1], img.shape[0], img.shape[2])
        tail = tailstr
        objs = data[i]

        def write_xml(anno_path, head, objs, tail):
            f = open(anno_path, "w")
            f.write(head)
            for i in range(len(objs['label'])):
                label = objs['label'][i]
                xmin = objs['left'][i]
                ymin = objs['top'][i]
                xmax = objs['left'][i]+objs['width'][i]
                ymax = objs['height'][i]+objs['top'][i]
                f.write(objstr % (label, xmin, ymin, xmax, ymax))
            f.write(tail)
        anno_path = 'data/svhn/Annotations/' + i.split(".")[0] + '.xml'
        write_xml(anno_path, head, objs, tail)
    print("DONE.")
