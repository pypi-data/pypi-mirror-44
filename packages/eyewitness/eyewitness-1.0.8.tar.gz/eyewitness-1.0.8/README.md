[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/eyewitness/badge/?version=latest)](https://eyewitness.readthedocs.io/)
[![PyPI Version](https://img.shields.io/pypi/v/eyewitness.svg)](https://pypi.org/project/eyewitness)
[![ci pipeline status](https://gitlab.com/penolove15/witness/badges/master/pipeline.svg)](https://gitlab.com/penolove15/witness/pipelines)



# EyeWitness
Lightweight Framework for object detection application.
wrapper your own detector and add your handler.

system design:
https://drive.google.com/file/d/1x_sCFs91swHR1Z3ofS4e2KFz6TK_kcHb/view?usp=sharing


document:
https://eyewitness.readthedocs.io/en/latest/index.html


## env
support python 2.7, 3.5, 3.6


## Installation
```bash
pip install eyewitness
```

manually installation
```bash
git clone https://gitlab.com/penolove15/witness.git
cd witness
python setup.py install
```


## TODO
- add examples using more model(wrapper with docker, survey for lightweight/ more accurate model)
- add image_puller for image collection. (consumer design)


## Things to be consider
[scale up]
- queuing system (how images pass(bytes(do by producer), file(queuing in fs))
- multiple detector


## Real Detector examples with docker
- MobileNet(caffe pre-trained) with cv2 [repo](https://github.com/penolove/cv2-object-detector)
- RefineDet implemented by [sfzhang15](https://github.com/sfzhang15/RefineDet) with caffe
- pelee implemented by [Robert-JunWang](https://github.com/Robert-JunWang/Pelee) with caffe
- MTCNN implemented by [DuinoDu](https://github.com/DuinoDu/mtcnn) with caffe
- RFB-SSD implemented by [lzx1413](https://github.com/lzx1413/PytorchSSD) with pytorch
- yolo-v3 implemented by [qqwweee](https://github.com/qqwweee/keras-yolo3) with keras
- Trident implemented by [TuSimple](https://github.com/TuSimple/simpledet) with mxnet
- Arcface implemented by [deepinsight](https://github.com/deepinsight/insightface) with mxnet

please take look at README.md inside docker/
there are examples wrapper a detection model
- pre-trained weighted
- naive example for detect a image
- end2end example with webcam
- evaluation with dataset


## DetectedResults Visualization project: Monitor Reporter
https://github.com/penolove/Flask-Monitor-Reporter

a flask UI used for visualization detection results.

![MonitorReporter](examples/MonitorReporter.png)


## [Developer] unit-test
```
nose2
```
