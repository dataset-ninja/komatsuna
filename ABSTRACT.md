The authors of the **KOMATSUNA** dataset present a 3D phenotyping platform designed to measure both plant growth and environmental information within small indoor environments, specifically tailored for plant image datasets. The primary objective is to create a comprehensive and compact platform using readily available commercial devices, enabling researchers to initiate plant phenotyping in their laboratories. The dataset showcased includes *rgb-d* and *multi-view* images depicting the early growth stages of Komatsuna, complete with leaf annotations.

## Motivation

Plant growth is influenced by various factors, including plant seeds, temperature, CO2, solar radiation, soil, and fertilizers. The appearance characteristics of a plant, known as its phenotype, result from the interplay between genetic properties and environmental conditions. Understanding this complex relationship is crucial for enhancing the quality and quantity of plant cultivation.

The authors meticulously selected the Komatsuna plant species for its growth properties, resilience to insects, and rapid growth in indoor environments. Hydroponic culture, chosen for its cleanliness and automation advantages, was adopted over traditional soil culture. The authors selected a hydroponic culture toolkit designed for small kitchen gardens, facilitating constant cultivation without daily maintenance.

<img src="https://github.com/dataset-ninja/komatsuna/assets/78355358/414db6d0-6c90-42bd-bea1-72e1fb5b3ae7" alt="image" width="400">

<span style="font-size: smaller; font-style: italic;">Platform to create KOMATSUNA datasets in indoor environments. To cultivate plants, a compact and complete platform for 3D plant phenotyping was developed using commercial devices only.</span>

## Lighting, Sensors and Cameras

Controlling lighting conditions is essential for indoor plant growth. The authors employed controllable switches for power sources, enabling programmable lighting durations. They utilized three types of lights—incandescent, fluorescent, and LED lights—opting for LED lights due to their controllability and spectrum composition. The Philips hue with programmable features was chosen, and its arrangement around the hydroponic culture toolkit was carefully considered.

To measure temperature, humidity, and light intensity, the authors utilized a Sony MESH device. This compact and cost-effective IoT device constantly measured and transferred data to a smartphone through Bluetooth. Lux was used as a simplified index for light intensity, although photosynthetic photon flux density (PPFD) is considered more appropriate for biological studies.

Two imaging systems were developed using an RGB-D camera (Intel RealSense SR300) and multiple high-resolution RGB cameras (FLIR cameras with Kowa lenses). The RGB-D camera was optimized for short-range capture, while the multiple RGB cameras addressed the low resolution of depth images, ensuring clear capture of plant shapes.

## Data Annotation

The manual annotation tool developed by the authors facilitates the creation of ground-truth labels for leaves in plant images on a pixel-by-pixel basis. This tool was designed to streamline the time-consuming task of annotation, incorporating various functions for efficient label creation.

Annotation process:

1. **Color Segmentation:** An initial mask for leaves was generated using thresholding-based binarization for each color channel, allowing for easy adjustment of threshold values. Users could adjust values by checking the generated mask superimposed onto the input image.

2. **Manual Segmentation:** To separate connected or overlapped leaves, a manual segmentation tool was implemented. Users could draw a freehand splitting curved line to divide one region into two with new leaf labels.

3. **Erasing:** An eraser tool was implemented to remove false positive regions in the initial mask, providing quick and easy removal of any size of false positive region.

4. **Label Assignment:** Each closed region in the mask was assigned one leaf label of a unique color. The label color was predefined and loaded into the tool. Users could fill a region with a colored label by selecting a label and clicking a pixel in the region. Additionally, a region label could be modified by clicking a pixel with another label.

## Dataset Creation

The authors generated two distinct datasets utilizing both an RGB-D camera and multiple RGB cameras publicly available on the web. Common and consistent environmental conditions were maintained across both datasets, with lighting, temperature, and humidity set at approximately 2400 lux, 28°C, and 30%, respectively. To expedite the growth of Komatsuna, lighting was provided continuously for 24 hours. In each dataset, images of five plants were captured every 4 hours over a span of 10 days. This allowed for the measurement of leaf shape and size changes in 3D space over both short and long terms.

In the **RGB-D dataset**, an RGB-D camera captured the entire hydroponic culture toolkit. Each plant region was manually segmented, forming individual plant images labeled in a label image. To facilitate temporal leaf tracking, consistent leaf labels were assigned to corresponding leaves in images captured at different times. The original camera resolution was 640 × 480, with plant images typically at 166 × 190 pixels. The alignment between RGB and depth images was crucial, considering the physical differences in viewpoints. To address this, a depth image was aligned into an RGB image, and the original depth image and transformation matrix were provided for further adjustments without interpolations.

The image name nomenclature and other file-specific descriptions can be found in the original [rgbd_README](https://limu.ait.kyushu-u.ac.jp/~agri/komatsuna/rgbd_readme.pdf)

The RGB-D camera's advantage lies in its ability to measure object shape even when lights are off, thanks to the emission of infrared lights. This facilitates the tracking of leaf movement for 24 hours, offering insights into the relationship between leaf shape and light source positions. Calibration of cameras and distances between them was achieved using a standard technique for 3D reconstruction.

In the **Multiview Dataset**, images of five plants were captured from three viewpoints and manually segmented into individual plant images. Similar to the RGB-D dataset, consistent leaf labels were assigned for spatial-temporal leaf tracking across different cameras and times. Unlike the RGB-D dataset, the ground truth for 3D shape was not measured due to the challenge of capturing more accurate 3D shapes than high-resolution multiple-view images. Future research may explore solutions, potentially involving RGB-D sensors. This dataset proves valuable for evaluating spatial-temporal instance segmentation across multiple views, addressing a gap where instance segmentation has traditionally been performed using single-view images. The authors suggest combining instance segmentation and stereo matching as a potential avenue for solving this challenge.

The image name nomenclature and other file-specific descriptions can be found in the original [multi_README](https://limu.ait.kyushu-u.ac.jp/~agri/komatsuna/multi_readme.pdf)