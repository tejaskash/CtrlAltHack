import cv2
import os
from tqdm import tqdm
i=1
imgdir = '~/Desktop/Azure/input/'

for img in tqdm(os.listdir(imgdir)):
    im = cv2.imread(img)
    filename = "fire."+str(i)+".jpg"
    cv2.imwrite(filename,im)

