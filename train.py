!pip install ngraph onednn

import numpy as np 
import pandas as pd
import os
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dropout, UpSampling2D, Concatenate, Input, Softmax
from tensorflow.keras import Model
from tensorflow.keras.callbacks import ModelCheckpoint
import ngraph as ng
import onednn as dnnl

EPOCHS=7
BATCH_SIZE=10
HEIGHT=256
WIDTH=256
N_CLASSES=13

def LoadImage(name, path):
    img = Image.open(os.path.join(path, name))
    img = np.array(img)
    
    image = img[:, :256]
    mask = img[:, 256:]
    
    return image, mask

def bin_image(mask):
    bins = np.array([20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240])
    new_mask = np.digitize(mask, bins)
    return new_mask

def getSegmentationArr(image, classes, width=WIDTH, height=HEIGHT):
    seg_labels = np.zeros((height, width, classes))
    img = image[:, :, 0]

    for c in range(classes):
        seg_labels[:, :, c] = (img == c).astype(int)
    return seg_labels

def give_color_to_seg_img(seg, n_classes=N_CLASSES):
    seg_img = np.zeros((seg.shape[0], seg.shape[1], 3)).astype('float')
    colors = sns.color_palette("hls", n_classes)
    
    for c in range(n_classes):
        segc = (seg == c)
        seg_img[:, :, 0] += (segc * (colors[c][0]))
        seg_img[:, :, 1] += (segc * (colors[c][1]))
        seg_img[:, :, 2] += (segc * (colors[c][2]))

    return seg_img

train_folder = "/content/drive/MyDrive/Intel OneAPI Hackathon Project/Dataset/cityscapes_paris/train"
valid_folder = "/content/drive/MyDrive/Intel OneAPI Hackathon Project/Dataset/cityscapes_paris/val"

num_of_training_samples = len(os.listdir(train_folder)) 
num_of_valid_samples = len(os.listdir(valid_folder))

def DataGenerator(path, batch_size=BATCH_SIZE, classes=N_CLASSES):
    files = os.listdir(path)
    while True:
        for i in range(0, len(files), batch_size):
            batch_files = files[i: i + batch_size]
            imgs = []
            segs = []
            for file in batch_files:
                image, mask = LoadImage(file, path)
                mask_binned = bin_image(mask)
                labels = getSegmentationArr(mask_binned, classes)

                imgs.append(image)
                segs.append(labels)

            yield np.array(imgs), np.array(segs)

train_gen = DataGenerator(train_folder, batch_size=BATCH_SIZE)
val_gen = DataGenerator(valid_folder, batch_size=BATCH_SIZE)

imgs, segs = next(train_gen)
imgs.shape, segs.shape

image = imgs[0]
mask = give_color_to_seg_img(np.argmax(segs[0], axis=-1))
masked_image = cv2.addWeighted(image/255, 0.5, mask, 0.5, 0)

fig, axs = plt.subplots(1, 3, figsize=(20, 20))
axs[0].imshow(image)
axs[0].set_title('Original Image')
axs[1].imshow(mask)
axs[1].set_title('Segmentation Mask')
axs[2].imshow(masked_image)
axs[2].set_title('Masked Image')
plt.show()

def conv2d_layer(x, filters, kernel_size=(3, 3), padding="same", strides=1):
    input_tensor = ng.constant(x, dtype=np.float32)
    filters_tensor = ng.constant(filters, dtype=np.float32)
    strides_tensor = ng.constant((1, strides, strides, 1), dtype=np.int32)
    padding_tensor = ng.constant(padding, dtype=np.string)

    input_shape = input_tensor.get_shape()
    filter_shape = filters_tensor.get_shape()

    input_tensor_reshaped = ng.reshape(input_tensor, (1, input_shape[0], input_shape[1], input_shape[2]))
    filters_tensor_reshaped = ng.reshape(filters_tensor, (filter_shape[0], filter_shape[1], input_shape[2], filter_shape[3]))

    output_shape = (input_shape[0], (input_shape[1] - 1) // strides + 1, (input_shape[2] - 1) // strides + 1, filter_shape[3])
    output_tensor = ng.tensor(output_shape, dtype=np.float32)

    conv_op = dnnl.convolution_forward(input_tensor_reshaped, filters_tensor_reshaped, strides_tensor, padding_tensor, output_tensor)
    conv_op.execute(dnnl.stream(), {
        input_tensor: input_tensor_reshaped,
        filters_tensor: filters_tensor_reshaped,
        output_tensor: output_tensor
    })

    return output_tensor.get_data().reshape(output_shape[1:])

def maxpool2d_layer(x, pool_size=(2, 2), strides=(2, 2)):
    input_tensor = ng.constant(x, dtype=np.float32)
    pool_size_tensor = ng.constant((1, pool_size[0], pool_size[1], 1), dtype=np.int32)
    strides_tensor = ng.constant((1, strides[0], strides[1], 1), dtype=np.int32)

    input_shape = input_tensor.get_shape()

    input_tensor_reshaped = ng.reshape(input_tensor, (1, input_shape[0], input_shape[1], input_shape[2]))

    output_shape = (input_shape[0], (input_shape[1] - pool_size[0]) // strides[0] + 1, (input_shape[2] - pool_size[1]) // strides[1] + 1, input_shape[3])
    output_tensor = ng.tensor(output_shape, dtype=np.float32)

    pool_op = dnnl.max_pooling_forward(input_tensor_reshaped, pool_size_tensor, strides_tensor, output_tensor)
    pool_op.execute(dnnl.stream(), {
        input_tensor: input_tensor_reshaped,
        output_tensor: output_tensor
    })

    return output_tensor.get_data().reshape(output_shape[1:])

def down_block(x, filters, kernel_size=(3, 3), padding="same", strides=1):
    c = conv2d_layer(x, filters, kernel_size, padding, strides)
    c = conv2d_layer(c, filters, kernel_size, padding, strides)
    p = maxpool2d_layer(c, pool_size=(2, 2), strides=(2, 2))
    return c, p

def up_block(x, skip, filters, kernel_size=(3, 3), padding="same", strides=1):
    us = UpSampling2D()(x)
    concat = Concatenate()([us, skip])
    c = conv2d_layer(concat, filters, kernel_size, padding, strides)
    c = conv2d_layer(c, filters, kernel_size, padding, strides)
    return c

def build_unet(input_shape, num_classes):
    inputs = Input(input_shape)
    
    c1, p1 = down_block(inputs, 16, kernel_size=(3, 3), padding="same")
    c2, p2 = down_block(p1, 32, kernel_size=(3, 3), padding="same")
    c3, p3 = down_block(p2, 64, kernel_size=(3, 3), padding="same")
    c4, p4 = down_block(p3, 128, kernel_size=(3, 3), padding="same")
    
    c5 = conv2d_layer(p4, 256, kernel_size=(3, 3), padding="same", strides=1)
    
    u6 = up_block(c5, c4, 128, kernel_size=(3, 3), padding="same", strides=1)
    u7 = up_block(u6, c3, 64, kernel_size=(3, 3), padding="same", strides=1)
    u8 = up_block(u7, c2, 32, kernel_size=(3, 3), padding="same", strides=1)
    u9 = up_block(u8, c1, 16, kernel_size=(3, 3), padding="same", strides=1)
    
    outputs = Conv2D(num_classes, (1, 1), padding="same", activation=Softmax(axis=-1))(u9)
    model = Model(inputs, outputs)
    return model

input_shape = (HEIGHT, WIDTH, 3)
model = build_unet(input_shape, N_CLASSES)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4), loss='categorical_crossentropy', metrics=['accuracy'])

checkpoint = ModelCheckpoint("model_weights.h5", save_weights_only=True, save_best_only=True, verbose=1)
model.fit(train_gen, validation_data=val_gen, steps_per_epoch=num_of_training_samples//BATCH_SIZE, validation_steps=num_of_valid_samples//BATCH_SIZE, epochs=EPOCHS, callbacks=[checkpoint])
