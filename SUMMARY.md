**EDD2020: Endoscopy Disease Detection and Segmentation** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the medical industry. 

The dataset consists of 386 images with 1251 labeled objects belonging to 10 different classes including *BE_bbox*, *BE*, *polyp_bbox*, and other: *polyp*, *suspicious_bbox*, *suspicious*, *HGD_bbox*, *HGD*, *cancer_bbox*, and *cancer*.

Images in the EDD2020 dataset have pixel-level instance segmentation and bounding box annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation task (only one mask for every class). All images are labeled (i.e. with annotations). There are no pre-defined <i>train/val/test</i> splits in the dataset. The dataset was released in 2020 by the <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">UK-IT-FR joint research team</span>.

<img src="https://github.com/dataset-ninja/edd2020/raw/main/visualizations/poster.png">
