import os 
import matplotlib.pyplot as plt
import cv2
from alg1_plaka_tespit import plaka_konum_don


#1. alg veri icleme
"""
veri = os.listdir("veriseti")
for image_url in veri:
    img= cv2.imread("veriseti/"+image_url)    # veriseti/1.jpg bgr degeri gönderiri
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = cv2.resize(img ,(500, 500))
    plt.imshow(img)
    plt.show()
    """

veri = os.listdir("veriseti")
for image_url in veri:
    img= cv2.imread("veriseti/"+image_url)    # veriseti/1.jpg bgr degeri gönderiri

    img = cv2.resize(img ,(500, 500))

    plaka = plaka_konum_don(img)
    x,y,w,h = plaka
    if(w>h):
        plaka_bgr = img[y:y+h, x:x+w].copy()
    else:
        plaka_bgr = img[y:y + w, x:x + h].copy()

    img = cv2.cvtColor(plaka_bgr, cv2.COLOR_BGR2RGB)

    plt.imshow(img)
    plt.show()