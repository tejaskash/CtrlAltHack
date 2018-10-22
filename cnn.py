import cv2
import numpy as np 
import os
from random import shuffle 
from tqdm import tqdm
import tflearn
import tensorflow as tf
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
#-------------------------------------------------------------------
TrainDir = "all/train/"
TestDir = "all/test/"
ImgSize = 50
LR = 1e-3
ModelName = 'dogsvscats-{}-{}.model'.format(LR, '2conv-basic')
def labelImg(img):
    wordLabel = img.split('.')[-3]
    if wordLabel == 'cat': 
        return [1,0]
    elif wordLabel == 'dog':
        return [0,1]
def createTrainData():
    trainingData = []
    for img in tqdm(os.listdir(TrainDir)):
        label = labelImg(img)
        path = os.path.join(TrainDir,img)
        img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img,(ImgSize,ImgSize))
        trainingData.append([np.array(img),np.array(label)])
    shuffle(trainingData)
    np.save('traindata.npy',trainingData)
    return trainingData
def createTestData():
    testData = []
    for img in tqdm(os.listdir(TestDir)):
        path = os.path.join(TestDir,img)
        imgNum = img.split('.')[0]
        img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img,(ImgSize,ImgSize))
        testData.append([np.array(img),imgNum])
    shuffle(testData)
    np.save('testdata.npy',testData)
    return testData
trainData = createTrainData()
testerData = createTestData()
#-----------------------------------------------------------------------------
tf.reset_default_graph()

convnet = input_data(shape=[None, ImgSize, ImgSize, 1], name='input')

convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 128, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet, 0.8)

convnet = fully_connected(convnet, 2, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(convnet, tensorboard_dir='log')

if os.path.exists('{}.meta'.format(ModelName)):
    model.load(ModelName)
    print("Model Loaded")
train = trainData[:-500]
test = testerData[:-500]

X = np.array([i[0] for i in train]).reshape(-1,ImgSize,ImgSize,1)
#Y = [i[1] for i in train]

testX = np.array([i[0] for i in test]).reshape(-1,ImgSize,ImgSize,1)
#testY = [i[1] for i in test].reshape(-1,ImgSize,ImgSize,1)

model.fit({'input': X}, {'targets': Y}, n_epoch=3, validation_set=({'input': testX}, {'targets': testY}), snapshot_step=500, show_metric=True, run_id=ModelName)

