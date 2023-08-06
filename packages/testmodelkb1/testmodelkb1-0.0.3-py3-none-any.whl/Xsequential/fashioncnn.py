# -*- coding: utf-8 -*-
"""
Test for Keras Image classification
"""
# TensorFlow and keras
import tensorflow as tf
import keras
from keras.preprocessing import image
from keras.utils import plot_model
from keras.models import load_model
import Xsequential

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

# import Fashion MINST from keras
fashion_mnist = keras.datasets.fashion_mnist

# divide datasets into train and evaluation

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# preprocess the data
# take a look at the images
plt.figure()
plt.imshow(train_images[2])
plt.colorbar()
plt.grid(False)

# scale the images
train_images = train_images / 255.0
test_images = test_images / 255.0

plt.figure()
# plt.imshow(train_images[1])
plt.imshow(train_images[100], cmap=plt.cm.binary)
plt.xlabel(class_names[train_labels[100]])

# build the model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


model.start_experiment("sirisha", "fashioncnn", "dataset_link", "sclink")
history = model.xfit(train_images, train_labels, epochs=2, batch_size=16)

model.save('fashioncnn.h5')