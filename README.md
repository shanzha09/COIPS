# COIPS: Computer-aided OCTA Image Processing System
## Introduction
_This is the office implementation of "A Deep Learning-based Quality Assessment and Segmentation System with a Large-scale Benchmark Dataset for Optical Coherence Tomographic Angiography Image"_  
We developed the computer aided OCTA image processing system (COIPS) in our research.This system is designed  to help ophthalmologist in quality assessment and FAZ segmantation of Optical Coherence Tomography angiography (OCTA) images based on deep learning. This system is able to transform OCTA image format, assess octa image quality, segment FAZ, quantify FAZ metrics and generate the result report automatically, which contributes to reducing the workload of ophthalmologists and saving their time.  
Our system show large generalization ability to be extended to all storage format OCTA images by conversion into unified PNG format for processing, assess and classify the images, segment and quantify FAZ and report the results automatically.  
Firstly, we constructed a large-scale dataset made it public available. Then, we trained five quality assessment model: ResNet-101, Inception-V3, EfficientNet-B7, SE-ResNeXt-101 & Swin-Transformer-Large and one FAZ segmentation model: UNet based on nnU-Net framework.  
**Quality assessment Dataset**  

| | sOCTA-3x3-10k | sOCTA-6x6-14k |  
|:----:| :----: | :----: |  
|Training set| 6915 | 9292 |  
|Testing set| 2965 | 4150 |  
|External testing 1| 300 | 300 |  
|External testing 2| 300 | 300 |  
|Total| 10480 | 14042 |   
  
**FAZ segmentation Dataset**  
  
| | sOCTA-3x3-1.1k-seg | dOCTA-6x6-1.1k-seg |
|:----:| :----: | :----: |
|Training set| 708 | 800 |
|Testing set| 304 | 343 |
|Total| 1101 | 1143 |  
  
**Quality assessment Result**  

| |ResNet-101|ResNet-101|SE-ResNeXt-101|SE-ResNeXt-101|EfficientNet-B7|EfficientNet-B7|Swin-T-Large|Swin-T-Large|Inception-V3|Inception-V3|  
|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|  
|Acc|84.91|83.59|86.65|89.64|87.06|85.48|91.18|82.74|89.18|85.89|  
|Pre|85.38|84.54|89.42|89.79|88.02|87.04|91.82|83.81|89.69|86.6|  
|AUC|0.90|0.91|0.96|0.98|0.93|0.92|0.98|0.96|0.97|0.97|  
|F1-score|84.80|83.78|86.58|89.67|87.14|85.55|91.26|82.78|89.23|85.95|  
  
**Requirement**

|Package|Version|  
|:----:|:----:|  
|Python|3.9.2|  
|Torch|1.8.1+cu111|
|Torchversion|0.9.1+cu111|
|timm|0.4.8|
|tqdm|4.59.0|
|termcolor|1.1.0|
|nnunet|1.6.6|
|numpy|1.20.1|
|opencv-contrib-python|4.5.1.48|
|pillow|8.1.2|
|SimpleITK|2.0.2|  
  
## Usage 
### Prepare data
The raw OCTA images that you want to process should be put into a folder named `raw_OCTA_images`.  
The following formats of OCTA image are accepted: `.png`, `_jpg`, `.tif`.  
  
### Clone the COIPS and download the trained models  
Install the requirement and clone this git, firstly. Then, download the trained models. The models are available at [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5111976.svg)](https://doi.org/10.5281/zenodo.5111976).  
  
### Check the config  
You need to change the setting in configure  i.e., `config.py`

### Run  
`python COIP_system.py`  

### Result  
please change dir to `report`

## About the dataset  
The large-scale OCTA dataset is available at [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5111972.svg)](https://doi.org/10.5281/zenodo.5111972)， [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5111975.svg)](https://doi.org/10.5281/zenodo.5111975).  
These datasets are public available, if you use the dataset or our system in your research, please cite our paper [A Deep Learning-based Quality Assessment and Segmentation System with a Large-scale Benchmark Dataset for Optical Coherence Tomographic Angiography Image](https://arxiv.org/abs/2107.10476). 

## Powered By
The author would like to say thanks to:  
[Swin Transformer](https://github.com/microsoft/Swin-Transformer.git)  
[nnU-Net](https://github.com/MIC-DKFZ/nnUNet.git)


## Citation
@misc{wang2021deep,
      title={A Deep Learning-based Quality Assessment and Segmentation System with a Large-scale Benchmark Dataset for Optical Coherence Tomographic Angiography Image}, 
      author={Yufei Wang and Yiqing Shen and Meng Yuan and Jing Xu and Bin Yang and Chi Liu and Wenjia Cai and Weijing Cheng and Wei Wang},
      year={2021},
      eprint={2107.10476},
      archivePrefix={arXiv},
      primaryClass={eess.IV}
}
