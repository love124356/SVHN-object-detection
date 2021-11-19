# SVHN-detection

This repository gathers the code for object detection on SVHN image from the [in-class CodaLab competition](https://competitions.codalab.org/competitions/35888?secret_key=7e3231e6-358b-4f06-a528-0e3c8f9e328e).

We use [YOLOv5](https://github.com/ultralytics/yolov5), an open source object detection architectures and models based on PyTorch, to train our model.
In this competition, we use YOLOv5m, YOLOv5l these two models and analysis the results.

## Reproducing Submission
We need to do some pre-preparation for training and testing on our custom dataset.

To reproduce my submission without retrainig, do the following steps:
1. [Requirement](#Requirement)
2. [Repository Structure](#Repository-Structure)
3. [Inference](#Inference)

## Hardware

Ubuntu 18.04.5 LTS

Intel® Core™ i7-3770 CPU @ 3.40GHz × 8

GeForce GTX 1080/PCIe/SSE2

Speed.ipynb: Google Colab

## Requirement
All requirements should be detailed in requirements.txt.

```env
$ conda create -n YOLOv5 python=3.7 -y
$ conda activate YOLOv5
$ cd SVHN-object-detection
$ conda install pytorch=1.10.0 torchvision=0.11.1 -c pytorch
$ pip install -r requirements.txt
```

Official images can be downloaded from [CodaLab competition](https://competitions.codalab.org/competitions/35888?secret_key=7e3231e6-358b-4f06-a528-0e3c8f9e328e#participate-get_data)


## Repository Structure

The repository structure is:
```
SVHN-object-detection(root)
  +-- data                       # all files and script used in the program 
  |   +-- hyps
  |   +-- scripts
  |   +-- svhn
      |   +-- Annotations        # training set .xml
          |   +-- 1.xml   
          |   +-- 2.xml   
          |   +-- 3.xml   
          |   +-- ......
      |   +-- test               # testing set .png  
          |   +-- 117.png  
          |   +-- 162.png 
          |   +-- 196.png  
          |   +-- ......
      |   +-- train              # training set .png /.txt
          |   +-- 1.png   
          |   +-- 1.txt   
          |   +-- 2.png 
          |   +-- 2.txt 
          |   +-- ......
      |   +-- trainval           # training and validation sets .png /.txt
          |   +-- 1.png   
          |   +-- 1.txt   
          |   +-- 2.png 
          |   +-- 2.txt 
          |   +-- ......
      |   +-- val                # validation set .png /.txt
          |   +-- 1.png   
          |   +-- 1.txt   
          |   +-- 2.png 
          |   +-- 2.txt 
          |   +-- ......
      |   +-- digitStruct.mat
      |   +-- json_to_VOC.py
      |   +-- mat_to_json.py     
      |   +-- MatTransform.json  
      |   +-- VOC_to_yolo.py
      |   +-- train_val_split.py
  |   +-- svhn.yaml
  +-- models
  +-- utils
  +-- runs
  |   +-- detect                 # run detect.py and testing .png /.txt save here.
      |   +-- labels
      |   +-- 1.png
      |   +-- 2.png
      |   +-- ......
  |   +-- train                  # run train.py and training info save here.
  +-- detect.py                  # model prediction
  +-- inference.py               # reproduce my submission file
  +-- train.py                   # for training model
  +-- hubconf.py
  +-- Speed.ipynb                # for testing detector speed
  +-- requirements.txt           # txt file for establishing the environment
```

## Dataset setting

You can use ```mat_to_json.py``` to parse 'digitStruct.mat' file to .json file and then use ```json_to_VOC.py``` transfer to VOC format. This can use in MMDetection.

Next, using  ```VOC_to_yolo.py``` to make training set .txt (about info) for YOLOv5.

```py
$ python data/svhn/mat_to_json.py
$ python data/svhn/json_to_VOC.py
$ python data/svhn/VOC_to_yolo.py
```

Finally, using ```train_val_split.py``` to split data, and it will *move* training and validation data to train and val folder respectively. The trainval folder will be empty.

```py
$ python data/svhn/train_val_split.py
```

## Training

Before training, you need to split training and validation sets. Next, modifying train and val path in ```data/svhn.yaml```. 

```yaml
train: data/svhn/train  # 26722 images
val: data/svhn/val  # 6680 images
nc: 10  # class number
names: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # class names
```

To train the model, run this command:

```py
$ python train.py --img 320  --epochs 100 --batch 16 --data svhn.yaml --weights yolov5m.pt
```

Trained model will be saved as ```runs/train/exp{int}/weights/best.pt```

All mAP and speed of experiments will be written in [Results](#Results).

## Inference

Please download [this model]() if you want to reproduce my submission file, and run above codes.

To reproduce my submission file or test the model you trained, run:

```py
$ python detect.py --source data/svhn/test/ --weights runs/train/exp{int}/weights/best.pt --conf 0.25 --save-conf --save-txt 
$ python inference.py --txt runs/detect/exp/labels/ --data data/svhn/test/
```

Prediction file will be saved as ```root/answer.json```

## Results

Our model achieves the following performance on :

|         | YOLOv5m | YOLOv5l |
|---------|---------|---------|
| mAP     | 0.410383 | 0.412982 |
| Speed   | 0.0692   | 0.0848 |

