# Omnis
Deep Learning for Everyone

------------------


## You have just found Omnis.

Omnis is a library of deep neural network applications, written in Python and capable of running on top of [Keras](https://github.com/keras-team/keras) and [Tensorflow](https://www.tensorflow.org/). It was developed with a focus on enabling fast application of deep learning.

Use Omnis if you need a deep learning library that:

- Is EASY to learn.
- Allows for easy and fast use.
- Supports CNN, LSTM, GAN applications.

Omnis is compatible with: __Python 3.6-3.7__.

------------------


## Deep Block

Omnis has been developed as a backend library of [Deep Block](https://deepblock.site). Deep Block is a platform where anyone can use AI technologies with ease. try [Deep Block](https://deepblock.site).

------------------


## Getting started: Implement a deep learning application with 4 lines of code!

The core data structure of Omnis is Application which is designed to be easy to use in each field.

Here is an `Image Classification` example with the [`Caltech 101`](http://www.vision.caltech.edu/Image_Datasets/Caltech101/) dataset:

```python
from omnis.application.image_processing.image_classification.image_classification import Image_Classification
```

Choose an application:

```python
image_classifier = Image_Classification(model_type = 'densenet121')
```

Prepare data:

```python
image_classifier.prepare_train_data(get_image_from='directory', data_path='101_ObjectCategories')
```

After preparing data, you can train your application:

```python
image_classifier.train(epochs = 40, batch_size = 16)
```

Now you can use the application to classify images:

```python
prediction_result = image_classifier.predict(data_path = '101_ObjectCategories/accordion')

print('predict labels')
print(prediction_result)
```

For a more in-depth tutorial about Omnis, you can check out:

In the [examples folder](https://github.com/mkh48v/omnis/tree/master/example) of the repository, you will find more applications.

------------------


## Installation

Before installing Omnis, please prepare NVIDIA GPU(s) and install TensorFlow GPU and Keras using conda.

Then, you can install Omnis itself. There are two ways to install Omnis:

- **Install Omnis from PyPI (recommended):**

If you don't use a conda virtual environment, you can run the command below (not recommended):

```sh
sudo pip install omnis
```

If you are using a conda virtual environment, you may want to avoid using sudo:

```sh
pip install omnis
```

- **Alternatively: install Omnis from the GitHub source:**

First, clone Omnis using `git`:

```sh
git clone https://github.com/mkh48v/omnis.git
```

 Then, `cd` to the Omnis folder and run the install command:
```sh
cd omnis
python setup.py install
```

------------------


## Guiding principles

- __Simplicity.__ Omnis pursues a simple architecture. Designing a software with simple architecture not only helps you to understand the code easily but also helps your painful debugging.

- __Easiness.__ Don't worry about complicated algorithms or theories or mathematics. Omnis will handle difficult stuffs for you. Just learn how to use deep neural networks and USE THIS!

- __Modularity.__ No spaghetti code!

------------------


## Why this name, Omnis?

Omnis means _EVERY_ in Latin. The goal of Omnis is to make deep learning technologies easier so that _EVERY_ one can use deep learning technologies without headache.

------------------
