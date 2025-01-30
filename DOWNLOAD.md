Dataset **KOMATSUNA** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzMzNThfS09NQVRTVU5BL2tvbWF0c3VuYS1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJIZHNYL09EN013Z1RpY1F6SCtBdXVVcm5VOHdBMWFpZ1poRGx6ZHk5RDVvPSJ9)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='KOMATSUNA', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://limu.ait.kyushu-u.ac.jp/~agri/komatsuna/).