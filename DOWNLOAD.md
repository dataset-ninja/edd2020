Please visit dataset [homepage](https://ieee-dataport.org/competitions/endoscopy-disease-detection-and-segmentation-edd2020#files) to download the data. 

Afterward, you have the option to download it in the universal supervisely format by utilizing the *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='EDD2020', dst_path='~/dtools/datasets/EDD2020.tar')
```
