# Udacity Self Driving Car > fixed-small
https://universe.roboflow.com/roboflow-gw7yv/self-driving-car

Provided by [Roboflow](https://roboflow.ai)
License: MIT

# Overview

The [original Udacity Self Driving Car Dataset](https://github.com/udacity/self-driving-car/tree/master/annotations) is missing labels for thousands of pedestrians, bikers, cars, and traffic lights. This will result in poor model performance. When used in the context of self driving cars, this could even lead to human fatalities.

We re-labeled the dataset to correct errors and omissions. We have provided convenient downloads in many formats including VOC XML, COCO JSON, Tensorflow Object Detection TFRecords, and more.

Some examples of labels missing from the original dataset:
![Examples of Missing Labels](https://i.imgur.com/A5J3qSt.jpg)

# Stats

The dataset contains 97,942 labels across 11 classes and 15,000 images. There are 1,720 null examples (images with no labels).

All images are 1920x1200 (download size ~3.1 GB). We have also provided a version downsampled to 512x512 (download size ~580 MB) that is suitable for most common machine learning models (including YOLO v3, Mask R-CNN, SSD, and mobilenet).

Annotations have been hand-checked for accuracy by Roboflow.

![Class Balance](https://i.imgur.com/bOFkueI.pnghttps://)

Annotation Distribution:
![Annotation Heatmap](https://i.imgur.com/NwcrQKK.png)

# Use Cases

Udacity is building an open source self driving car! You might also try using this dataset to do person-detection and tracking.

# Using this Dataset

Our updates to the dataset are released under the MIT License (the same license as [the original annotations and images](https://github.com/udacity/self-driving-car/tree/master/annotations)).

**Note:** the dataset contains many duplicated bounding boxes for the same subject which we have not corrected. You will probably want to filter them by taking the IOU for classes that are 100% overlapping or it could affect your model performance (expecially in stoplight detection which seems to suffer from an especially severe case of duplicated bounding boxes).

# About Roboflow

[Roboflow](https://roboflow.ai) makes managing, preprocessing, augmenting, and versioning datasets for computer vision seamless.

Developers reduce 50% of their boilerplate code when using Roboflow's workflow, save training time, and increase model reproducibility.
:fa-spacer:
#### [![Roboflow Wordmark](https://i.imgur.com/WHFqYSJ.png =350x)](https://roboflow.ai)