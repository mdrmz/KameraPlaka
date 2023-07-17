import serial

ser = serial.Serial('COM6', 9600)




def Mesafe_Gönder():
    while True:
        if ser.in_waiting > 0:
            distance = ser.readline().decode('utf-8').rstrip()
            print("Mesafe:", distance, "cm")
            return  distance

