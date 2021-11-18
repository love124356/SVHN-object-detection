import os
import h5py
import json


bbox_prop = ['height', 'left', 'top', 'width', 'label']


def get_img_name(f, idx=0):
    img_name = ''.join(map(chr, f[names[idx][0]][()].flatten()))
    return(img_name)


def get_img_boxes(f, idx=0):
    """
    get the 'height', 'left', 'top', 'width', 'label' of
    bounding boxes of an image.
    :param f: h5py.File
    :param idx: index of the image
    :return: dictionary
    """
    meta = {key: [] for key in bbox_prop}

    box = f[bboxs[idx][0]]
    for key in box.keys():
        if box[key].shape[0] == 1:
            meta[key].append(int(box[key][0][0]))
        else:
            for i in range(box[key].shape[0]):
                meta[key].append(int(f[box[key][i][0]][()].item()))

    return meta


if __name__ == "__main__":
    digit_file = os.path.join('data/svhn/digitStruct.mat')
    print("Open .mat")
    f = h5py.File(digit_file, 'r')

    names = f['digitStruct/name']
    bboxs = f['digitStruct/bbox']

    """
    annotations = {
        "/path/to/images/000001.jpg": [
            {"bbox": ..., "label": ...},
            ...
        ],
        ...
    }
    """

    annotations = {}
    for i in range(bboxs.shape[0]):
        name = get_img_name(f, i)
        annotations[name] = get_img_boxes(f, i)

    # Write the list to answer.json
    json_object = json.dumps(annotations)

    with open("data/svhn/MatTransform.json", "w") as outfile:
        outfile.write(json_object)

    print("DONE.")
