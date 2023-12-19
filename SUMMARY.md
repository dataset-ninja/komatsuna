**KOMATSUNA Dataset for Instance Segmentation, Tracking and Reconstruction** is a dataset for instance segmentation, semantic segmentation, object detection, and monocular depth estimation tasks. It is used in the biological research. 

The dataset consists of 1560 images with 6184 labeled objects belonging to 1 single class (*leaf*).

Images in the KOMATSUNA dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. There are 360 (23% of the total) unlabeled images (i.e. without annotations). There are 2 splits in the dataset: *multi-view* (1080 images) and *rgb-d* (480 images). Alternatively, the dataset could be split into 6 image splits: ***multi_plant*** (900 images), ***rgbd_plant*** (300 images), ***multi_original*** (180 images), ***rgbd_depth*** (60 images), ***rgbd_depth_ours*** (60 images), and ***rgbd_original*** (60 images). Additionally, images are grouped by ***im_id***, and every *leaf* has ***old*** tag. Explore it in supervisely labeling tool. The dataset was released in 2017 by the Kyushu University, Japan.

<img src="https://github.com/dataset-ninja/komatsuna/raw/main/visualizations/poster.png">
