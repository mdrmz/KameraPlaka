import cv2
import time
import matplotlib.pyplot as plt
import numpy as np


def plaka_konum_don(img):
    img_bgr = img
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # islem resmi ir_img

    ir_img = cv2.medianBlur(img_gray, 5)  # 5x5
    ir_img = cv2.medianBlur(ir_img, 5)  # 5x5

    medyan = np.median(ir_img)

    low = 0.67 * medyan
    high = 1.33 * medyan

    # Jonh f Canny
    kenarlik = cv2.Canny(ir_img, low, high)

    # np.ones((3,3),np.uint8) -->
    kenarlik = cv2.dilate(kenarlik, np.ones((3, 3), np.uint8), iterations=1)

    # cv2.RETR_TREE -> hiyeralsık
    # CHAIN_APPROX_SIMPLE -> kosegenleri aldık, tum pıkseller yerine
    cnt = cv2.findContours(kenarlik, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = cnt[0]
    cnt = sorted(cnt, key=cv2.contourArea, reverse=True)

    H, W = 500, 500
    plaka = None

    for c in cnt:
        rect = cv2.minAreaRect(c)  # dikdortgen yapıda al (1)
        (x, y), (w, h), r = rect
        if (w > h and w > h * 2) or (h > w and h > w * 2):  # oran en az 2 (2)
            box = cv2.boxPoints(rect)  # [[12,13],[25,13],[20,13],[13,45]]
            box = np.int64(box)

            minx = np.min(box[:, 0])
            miny = np.min(box[:, 1])
            maxx = np.max(box[:, 0])
            maxy = np.max(box[:, 1])

            muh_plaka = img_gray[miny:maxy, minx:maxx].copy()
            muh_medyan = np.median(muh_plaka)

            kon1 = muh_medyan > 84 and muh_medyan < 200  # yogunluk kontrolu (3)
            kon2 = h < 50 and w < 150  # sınır kontrolu (4)
            kon3 = w < 50 and h < 150  # sınır kontrolu (4)

            print(f"muh_plaka medyan:{muh_medyan} genislik: {w} yukseklik:{h}")

            kon = False
            if (kon1 and (kon2 or kon3)):
                # plaka'dır

                # cv2.drawContours(img,[box],0,(0,255,0),2)
                plaka = [int(i) for i in [minx, miny, w, h]]  # x,y,w,h
                kon = True
            else:
                # plaka değidir
                # cv2.drawContours(img,[box],0,(0,0,255),2)
                pass
            if (kon):
                return plaka
    return []

cap = cv2.VideoCapture(1)

pTime = 0
cTime = 0

while True:
    success ,img = cap.read()

    img = cv2.resize(img, (500, 500))
    plaka = plaka_konum_don(img)
    x, y, w, h = plaka
    if (w > h):
        plaka_bgr = img[y:y + h, x:x + w].copy()
       # cv2.imwrite("plaka.jpg",plaka_bgr)
    else:
        plaka_bgr = img[y:y + w, x:x + h].copy()

    img = cv2.cvtColor(plaka_bgr, cv2.COLOR_BGR2RGB)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)


    #cv2.imshow('poı',img)
    #cv2.waitKey(1)
    #plt.show()