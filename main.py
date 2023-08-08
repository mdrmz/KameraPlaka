import os
import random
import string
import sys
from datetime import datetime
from VideoCapture import  Camera

import cv2  # Add the cv2 import
import pandas as pd
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtGui import (QIcon, QImage,  # Add QImage import; Add this line
                         QPixmap, QStandardItemModel, QTextCursor)
from PyQt5.QtWidgets import (QApplication, QDialog, QGraphicsScene,
                             QGraphicsView, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton, QTextEdit,
                             QVBoxLayout)

app = QtWidgets.QApplication([])
ui = uic.loadUi("GUI.ui")

# With this line:
ui.graphicsViewCamera.setObjectName("graphicsViewCamera")

# Initialize camera
camera = Camera()  # 0 for the default camera

# Function to capture and update the camera feed
def update_camera_feed():
    global camera
    ret, frame = camera.read()  # Capture a frame from the camera

    if ret:
        # Convert the frame from OpenCV BGR format to QImage
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        q_img = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Display the QImage in the QGraphicsView widget
        pixmap = QPixmap.fromImage(q_img)
        scene = QGraphicsScene()  # Create a new QGraphicsScene
        scene.addPixmap(pixmap)  # Add the QPixmap to the scene
        ui.graphicsViewCamera.setScene(scene)  # Set the scene for graphicsViewCamera

        # Set the viewport anchor to ensure the image fits fully into the view
        ui.graphicsViewCamera.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        ui.graphicsViewCamera.setResizeAnchor(QGraphicsView.AnchorUnderMouse)


# Call the update_camera_feed function periodically to continuously update the camera feed
camera_timer = QTimer()
camera_timer.timeout.connect(update_camera_feed)
camera_timer.start(50)  # Update every 50 milliseconds (adjust as needed)


def load_and_display_image(image_path):
    # Check if the image file exists
    if not os.path.exists(image_path):
        print("Image file not found.")
        return

    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image is None:
        print("Failed to load the image.")
        return

    # Convert the image from OpenCV BGR format to QImage
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, channels = rgb_image.shape
    bytes_per_line = channels * width
    q_img = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)

    # Display the QImage in the QGraphicsView widget
    pixmap = QPixmap.fromImage(q_img)
    scene = QGraphicsScene()  # Create a new QGraphicsScene
    scene.addPixmap(pixmap)  # Add the QPixmap to the scene
    ui.graphicsView_2.setScene(scene)  # Set the scene for graphicsView_2

    # Set the viewport anchor to ensure the image fits fully into the view
    ui.graphicsView_2.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    ui.graphicsView_2.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

# Example usage:
image_path = "OnlyPlate"
load_and_display_image(image_path)


# Avrupa standartlarına uygun rastgele plaka oluşturucu
def generate_random_plate():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=2))
    lastNumbers = ''.join(random.choices(string.digits, k=3))
    return f"{numbers} {letters} {lastNumbers}"

# Örnek veriler
sample_data = [
    {"nameSurname": "Liam White", "isRegistered": True, "Time": "22:15", "plateNumber": generate_random_plate()},
    {"nameSurname": "Olivia Green", "isRegistered": False, "Time": "06:30", "plateNumber": generate_random_plate()},
    {"nameSurname": "Noah Turner", "isRegistered": True, "Time": "11:45", "plateNumber": generate_random_plate()},
    {"nameSurname": "Emma Brown", "isRegistered": False, "Time": "09:55", "plateNumber": generate_random_plate()},
    {"nameSurname": "Oliver Wilson", "isRegistered": True, "Time": "14:35", "plateNumber": generate_random_plate()},
    {"nameSurname": "Ava Martinez", "isRegistered": True, "Time": "16:40", "plateNumber": generate_random_plate()},
    {"nameSurname": "Elijah Clark", "isRegistered": False, "Time": "17:25", "plateNumber": generate_random_plate()},
    {"nameSurname": "Isabella Mitchell", "isRegistered": True, "Time": "08:05", "plateNumber": generate_random_plate()},
    {"nameSurname": "Lucas Turner", "isRegistered": True, "Time": "12:15", "plateNumber": generate_random_plate()},
    {"nameSurname": "Mia Smith", "isRegistered": False, "Time": "15:05", "plateNumber": generate_random_plate()},
    {"nameSurname": "Oliver Wilson", "isRegistered": True, "Time": "16:40", "plateNumber": generate_random_plate()},
    {"nameSurname": "Eva Martinez", "isRegistered": True, "Time": "16:50", "plateNumber": generate_random_plate()},
    {"nameSurname": "James Adams", "isRegistered": False, "Time": "10:11", "plateNumber": generate_random_plate()},
    {"nameSurname": "Sophia Turner", "isRegistered": True, "Time": "18:20", "plateNumber": generate_random_plate()},
    {"nameSurname": "William Lee", "isRegistered": False, "Time": "21:55", "plateNumber": generate_random_plate()},
    {"nameSurname": "Avery Johnson", "isRegistered": True, "Time": "05:10", "plateNumber": generate_random_plate()},
    {"nameSurname": "Alexander Clark", "isRegistered": False, "Time": "07:25", "plateNumber": generate_random_plate()},
    {"nameSurname": "Abigail Turner", "isRegistered": True, "Time": "14:05", "plateNumber": generate_random_plate()},
    {"nameSurname": "Mason Smith", "isRegistered": True, "Time": "13:55", "plateNumber": generate_random_plate()},
    {"nameSurname": "Harper Wilson", "isRegistered": False, "Time": "12:25", "plateNumber": generate_random_plate()}
]

# Function to update the table view with the data
def update_table_view():
    global sample_data, model
    model.clear()
    sorted_sample_data = sorted(sample_data, key=lambda x: datetime.strptime(x["Time"], '%H:%M'), reverse=True)
    for row, data in enumerate(sorted_sample_data):
        for col, item in enumerate(data.values()):
            if col == 2:  # 3. sütun (Saat) için özel işlem yapacağız
                time_str = item
                try:
                    time_obj = datetime.strptime(time_str, '%H:%M')  # Saat verisini datetime nesnesine dönüştürüyoruz
                    # Şimdi zamanı 24 saatlik dilime göre yeniden biçimlendireceğiz
                    item = time_obj.strftime('%H:%M')
                except ValueError:
                    pass  # Hatalı bir saat formatı olduğunda işlemi geçiyoruz
            model.setItem(row, col, QtGui.QStandardItem(str(item)))

# Butona tıklandığında bir giriş formu açmak için fonksiyon
def show_input_form():
    input_form = QDialog()
    input_form.setWindowTitle("Araç Kaydet")
    layout = QVBoxLayout(input_form)

    name_label = QLabel("İsim Soyisim:")
    name_edit = QLineEdit()
    layout.addWidget(name_label)
    layout.addWidget(name_edit)

    status_label = QLabel("Kayıtlı/Misafir:")
    status_edit = QLineEdit()
    layout.addWidget(status_label)
    layout.addWidget(status_edit)

    time_label = QLabel("Saat (HH:MM):")
    time_edit = QLineEdit()
    layout.addWidget(time_label)
    layout.addWidget(time_edit)

    plate_label = QLabel("Araç Plakası:")
    plate_edit = QLineEdit()
    layout.addWidget(plate_label)
    layout.addWidget(plate_edit)

    add_button = QPushButton("Ekle")
    layout.addWidget(add_button)

    def add_data_to_table():
        global sample_data, model
        name = name_edit.text()
        status = status_edit.text()
        time = time_edit.text()
        plate = plate_edit.text()

        # Saat bilgisinin doğru formatta girildiğinden emin olun
        try:
            datetime.strptime(time, '%H:%M')
        except ValueError:
            QMessageBox.critical(input_form, "Hata", "Lütfen saat formatını (HH:MM) olarak girin.", QMessageBox.Ok)
            return

        # Giriş verilerini sample_data listesine ekleyin
        sample_data.append({"nameSurname": name, "isRegistered": True if status.lower() == "true" else False, "Time": time, "plateNumber": plate})

        # tableView'i güncellenmiş sample_data ile yenileyin
        update_table_view()

        input_form.close()  # Giriş formunu verileri tableView'e ekledikten sonra kapatın

    add_button.clicked.connect(add_data_to_table)

    input_form.exec()

# Butonun tıklama olayını giriş formunu açmak için bağlayın
ui.pushButton_1.clicked.connect(show_input_form)

# Function to show a pop-up window when the button is clicked
def show_popup_message():
    message_box = QMessageBox()
    message_box.setText("*KAYITLAR*")
    message_box.setWindowTitle("Kayıt Düzenle")
    message_box.setIcon(QMessageBox.Information)
    message_box.exec()

# Connect the button clicks to the function
ui.pushButton_2.clicked.connect(show_popup_message)  # Replace 'pushButton' with the actual name of the push button in your UI

# Function to show a pop-up window when the button is clicked
def show_popup_message():
    message_box = QMessageBox()
    message_box.setText("*KAYITLAR*")
    message_box.setWindowTitle("Kayıt Sil")
    message_box.setIcon(QMessageBox.Information)
    message_box.exec()

# Connect the button clicks to the function
ui.pushButton_3.clicked.connect(show_popup_message)  # Replace 'pushButton' with the actual name of the push button in your UI

gateStatus = False  # Initialize gateStatus as False

# Function to show a pop-up window when the button is clicked
def show_popup_message():
    global report_window, gateStatus  # Reference the global variables

    # Check if the gate is already open (gateStatus is True)
    if gateStatus:
        # Show the "Kapı Zaten Açık" message
        message_box = QMessageBox()
        message_box.setText("Kapı Zaten Açık!")
        message_box.setWindowTitle("Kapı Durumu")
        message_box.setIcon(QMessageBox.Information)
        message_box.exec()
        return  # Return without changing gateStatus or showing "Kapı Açılıyor" message

    # If the gate is closed (gateStatus is False), show the "Kapı Açılıyor" message
    message_box = QMessageBox()
    message_box.setText("Kapı Açılıyor...")
    message_box.setWindowTitle("Giriş Kontrol")
    message_box.setIcon(QMessageBox.Information)
    message_box.exec()

    # Update the gate status to True
    gateStatus = True

# Connect the button clicks to the function
ui.pushButton_4.clicked.connect(show_popup_message)


# Function to show a pop-up window when the button is clicked
def show_popup_message():
    global report_window, gateStatus  # Reference the global variables

    # Check if the gate is already closed (gateStatus is False)
    if not gateStatus:
        # Show the "Kapı Zaten Kapalı" message
        message_box = QMessageBox()
        message_box.setText("Kapı Zaten Kapalı!")
        message_box.setWindowTitle("Kapı Durumu")
        message_box.setIcon(QMessageBox.Information)
        message_box.exec()
        return  # Return without changing gateStatus or showing "Kapı Kapatılıyor" message

    # If the gate is open (gateStatus is True), show the "Kapı Kapatılıyor" message
    message_box = QMessageBox()
    message_box.setText("Kapı Kapatılıyor...")
    message_box.setWindowTitle("Giriş Kontrol")
    message_box.setIcon(QMessageBox.Information)
    message_box.exec()

    # Update the gate status to False
    gateStatus = False

# Connect the button clicks to the function
ui.pushButton_5.clicked.connect(show_popup_message)

# Function to show a pop-up window when the button is clicked
def show_popup_message():
    global report_window  # Reference the global variable

    # Check the gateStatus and show the appropriate message
    if gateStatus:
        message_text = "Kapı Açık."
    else:
        message_text = "Kapı Kapalı."

    # Create the message box
    message_box = QMessageBox()
    message_box.setText(message_text)
    message_box.setWindowTitle("Kapı Durumu")
    message_box.setIcon(QMessageBox.Information)
    message_box.exec()

def show_popup_message():
    global report_window  # Reference the global variable

    # Create the confirmation message box
    message_box = QMessageBox()
    message_box.setText("Günlük Rapor istediğinize emin misiniz?")
    message_box.setWindowTitle("Z Raporu")
    message_box.setIcon(QMessageBox.Information)
    yes_button = message_box.addButton(QMessageBox.Yes)
    no_button = message_box.addButton(QMessageBox.No)

    # Show the message box and wait for the user's response
    result = message_box.exec()

    if result == QMessageBox.Yes:
        # Show tableView data in a new window
        report_window = QDialog()
        report_window.setWindowTitle("Günlük Rapor")
        layout = QVBoxLayout(report_window)
        report_text_edit = QTextEdit()
        report_text_edit.setPlainText(get_table_data())
        layout.addWidget(report_text_edit)

        # Add "İptal" and "Raporla" buttons to the new window
        button_layout = QHBoxLayout()
        cancel_button = QPushButton("İptal")
        report_button = QPushButton("Raporla")
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(report_button)
        layout.addLayout(button_layout)

        # Connect the buttons to their respective functions
        cancel_button.clicked.connect(report_window.close)
        report_button.clicked.connect(save_to_excel)

        report_window.exec()

    elif result == QMessageBox.No:
        # If the user clicked "No", just close the message box
        message_box.close()

def get_table_data():
    # Function to retrieve the data from the tableView and return it as a string
    # Replace this function with your code to fetch the data from the tableView
    data = ""
    for row in range(model.rowCount()):
        for col in range(model.columnCount()):
            item = model.item(row, col)
            data += f"{item.text()}\t"
        data += "\n"
    return data

def save_to_excel():
    data = get_table_data()

    # Format the data as a dictionary
    formatted_data = {"İsim Soyisim": [], "Kayıtlı/Misafir": [], "Saat": []}
    for row in data.split("\n"):
        if row.strip():  # Skip empty lines
            name, status, time = row.strip().split("\t")
            formatted_data["İsim Soyisim"].append(name)
            formatted_data["Kayıtlı/Misafir"].append(status)
            formatted_data["Saat"].append(time)

    # Convert the formatted data to a DataFrame
    df = pd.DataFrame(formatted_data)

    # Save the DataFrame to an Excel file
    df.to_excel("log.xlsx", index=False)

    if report_window:
        report_window.close()  # Close the report window after saving the data to the Excel file



# Connect the button clicks to the function
ui.pushButton_6.clicked.connect(show_popup_message)

# Saat verilerini datetime nesnesine dönüştürerek sıralama işlemi
sorted_sample_data = sorted(sample_data, key=lambda x: datetime.strptime(x["Time"], '%H:%M'), reverse=True)

# Verileri eklemek için bir model oluşturuyoruz.
model = QtGui.QStandardItemModel()  # Use QtGui instead of QtWidgets

# Tablonun başlıklarını ayarlıyoruz.
model.setHorizontalHeaderLabels(["İsim Soyisim", "Kayıt", "Saat", "Araç Plakası"])

# Örnek verileri modele ekliyoruz.
for row, data in enumerate(sorted_sample_data):
    for col, item in enumerate(data.values()):
        if col == 2:  # 3. sütun (Saat) için özel işlem yapacağız
            time_str = item
            try:
                time_obj = datetime.strptime(time_str, '%H:%M')  # Saat verisini datetime nesnesine dönüştürüyoruz
                # Şimdi zamanı 24 saatlik dilime göre yeniden biçimlendireceğiz
                item = time_obj.strftime('%H:%M')
            except ValueError:
                pass  # Hatalı bir saat formatı olduğunda işlemi geçiyoruz
        model.setItem(row, col, QtGui.QStandardItem(str(item)))

# Tabloya modeli bağlıyoruz.
ui.tableView.setModel(model)

# Remove horizontal scroll bars from the tableView
ui.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

# Resize rows and columns to fit contents
ui.tableView.resizeRowsToContents()
ui.tableView.resizeColumnsToContents()

def clock():
    currentTime = QTime.currentTime()
    currentTimeText = currentTime.toString('hh:mm:ss')
    ui.lcdClock.display(currentTimeText)

# Create a QTimer and connect it to the clock function
clock_timer = QTimer()
clock_timer.timeout.connect(clock)
clock_timer.start(1000)  # Update every 1000 milliseconds (1 second)


# Connect the camera timer to the UI window's show event
ui.showEvent = lambda event: camera_timer.start(50)  # Update every 50 milliseconds (adjust as needed)

ui.show()
app.exec()