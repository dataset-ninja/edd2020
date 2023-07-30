**EDD2020: Endoscopy Disease Detection and Segmentation** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the medical industry. 



The dataset consists of 772 images with 1251 labeled objects belonging to 10 different classes including *BE_bbox*, *BE*, *polyp_bbox*, and other: *polyp*, *suspicious_bbox*, *suspicious*, *HGD_bbox*, *HGD*, *cancer_bbox*, and *cancer*.

Images in the EDD2020 dataset have pixel-level instance segmentation and bounding box annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation task (only one mask for every class). All images are labeled (i.e. with annotations). There are 2 splits in the dataset: *bbox* (386 images) and *masks* (386 images). The dataset was released in 2020 by the [UK-FR-IT joint research group](https://ieee-dataport.org/competitions/endoscopy-disease-detection-and-segmentation-edd2020#files).

Here are the visualized examples for each of the 10 classes:

[Dataset classes](https://github.com/dataset-ninja/edd2020/raw/main/visualizations/classes_preview.webm)
