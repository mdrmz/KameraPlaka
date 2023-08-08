import cv2

def Camera():
    cap = cv2.VideoCapture(0)
    return cap

def TakeaPhoto():

    i = 0
    cap = cv2.VideoCapture(0)
    while True:
        success ,img = cap.read()
        cv2.imwrite(f"OnlyPlate/{i}.jpg",img)
        i+=1

