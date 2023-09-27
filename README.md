<h1 align='center'>White Matter Detection in the Brain</h1>
___

## Table of Contents:
1. [Scientific Background](#1)
2. [Project Summary](#2)
3. [Instructions to Run App Locally](#3)
4. [Additional Information](#4)


<h2 align='center'>Scientific Background<a name='1'></a></h2>

### What is white matter?:
White matter is the part of the brain that is heavily enriched in myelin, a fatty substance that causes increased signal transduction across the neurons using saltatory conduction. 

For more information on myelin refer to this <a href='https://www.nationalmssociety.org/What-is-MS/Definition-of-MS/Myelin'>link</a> by the National MS Society

<p align='center'>
	<img src='https://miykael.github.io/nipype-beginner-s-guide/_images/GM.gif'></img>
</p>

<h2 align='center'>Project Summary:<a name='2'></a></h2>

### Goal:
>This project is to create an application that can detect the structural differences in white matter using deep learning for predicting age.

There will be two parts to this project:

### 1. Modeling Portion: <a href='https://github.com/johnnys7n/DetectingBrainWhiteMatterChanges/tree/main/Modeling'>link</a>
In this portion, I have compiled images from immunohistochemistry experiments (sample images in the `/sample_data` folder to see how the images look like, referenced from <a href='https://www.researchgate.net/figure/Normal-CNS-morphology-and-myelination-in-Dars-mice-A-and-B-Paraffin-embedded_fig5_309660386'>link</a>) and decided to see if a image classification algorithm using deep learning convolutional neural network (specifically TensorFlow Hub's `mobilenet_v2_130_224`) can predict the structural changes and also predict the type of neurodegeneration. The modeling portion is still on its very early experiment phases and only got ~65% model accuracy. I am in the process of acquiring more data.  

For more information on the model here is a <a href='https://tfhub.dev/google/imagenet/mobilenet_v2_130_224/classification/5'>link!</a>
	
### 2. Deployment Portion: <a href='https://github.com/johnnys7n/DetectingBrainWhiteMatterChanges/tree/main/app'>link</a>

This section will be using Flask to deploy the model for testing. (Still under progress). The currently working app will only detect contour differences between two brain images using Scikit-image and OpenCV's contour analysis. This app does not integrate the model output yet and will be planning on doing so once the model achieves a certain level of classification accuracy. This portion was more so to see if a simple computer vision can detect regional changes in myelination that reflects the true changes in biological phenomena. 

<h2 align='center'>Instructions to Run App Locally<a name='3'></a></h2>

#### Step to run application:
* Step 1: Create the copy of the project.
* Step 2: Open command prompt and change your current path to folder where you can find 'app.py' file.
* Step 3: Create environment by command given below:
	conda create -name <environment name>
* Step 4: Activate environment by command as follows:
	conda activate <environment name>
* Step 5: Use command below to install required dependencies:
	python -m pip install -r requirements.txt
* Step 6: Run application by command:
	**python app.py**
You will get url copy it and paste in browser.
* Step 7: Lastly Test your images.

<h2 align='center'>Additional Information<a name='2'></a></h2>

* Outputing the regional anatomical areas of the brain and its specific structural similarity score (ie. Thalamus, Hippocampus, Corpus Callosum, Cortex, etc)
* Training a set of images to classify areas of the brain that are "sick" 
* Train tensor models for detecting regional changes
