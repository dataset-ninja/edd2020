Dataset **EDD2020** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzE5NzVfRUREMjAyMC9lZGQyMDIwLURhdGFzZXROaW5qYS50YXIiLCAic2lnIjogIm5FL1B4TjllM3U4WkFFRUxtUHp2Zms5Tm44L3M4czJSakpSM2tQcmRGREE9In0=)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='EDD2020', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://ieee-dataport.s3.amazonaws.com/competition/6486/EndoCV2020-Endoscopy-Disease-Detection-Segmentation-subChallenge_data.zip?response-content-disposition=attachment%3B%20filename%3D%22EndoCV2020-Endoscopy-Disease-Detection-Segmentation-subChallenge_data.zip%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJOHYI4KJCE6Q7MIQ%2F20230911%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230911T193359Z&X-Amz-SignedHeaders=Host&X-Amz-Expires=86400&X-Amz-Signature=584a80f54dd7c2aebb2f8a6fa989c9fb1ce3f810e303b60878d306695275de40).