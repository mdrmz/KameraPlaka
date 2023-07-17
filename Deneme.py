import cv2
import matplotlib.pyplot as plt
import numpy as np
from Arduinp_serial import Mesafe_Gönder
import os

cap = cv2.VideoCapture(1)
i = 0
kon = False

while True:

    success , img = cap.read()
    deger = Mesafe_Gönder()
    deger = int(deger)
    if( deger < 30 and deger > 10 ):
        cv2.imshow("ing", img)
        cv2.imwrite(f"ar/{i}.jpg", img)

        if (kon):
            cv2.destroyAllWindows()
            i = i+1
        kon = True
        cv2.waitKey(1)










