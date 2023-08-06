import datetime as dt
import pandas as pd
import numpy as np
import keras
import os
import tensorflow as tf
from matplotlib import pyplot as plt
from sklearn.metrics import *
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD
from keras.applications.vgg16 import VGG16



def confusionmatrix(labels, y_pred):
    """

    :param labels: True class labels
    :param y_pred: Predicted class labels
    :return: confusion matrix

    """
    cf_matrix = confusion_matrix(labels.argmax(axis=1), y_pred.argmax(axis=1))
    return cf_matrix

def auroc(labels,y_pred):
    """

    :param labels: True class labels
    :param y_pred: Predicted class labels
    :return: Area under ROC Curve value

    """
    return tf.py_func(roc_auc_score, (labels,y_pred,tf.double))

def print_roc(labels,y_pred):
    """
    * Prints the Area under ROC Curve value
    """
    print(roc_auc_score(labels, y_pred))


def print_classification_report(labels,y_pred):
    """

    :param labels: True class labels
    :param y_pred: Predicted class labels
    :return: Classification Report with  Precision, Recall, Specificity and F1 Score

    """
    class_report = classification_report(y_true= labels.argmax(axis=1), y_pred= y_pred.argmax(axis=1))
    print(class_report)





