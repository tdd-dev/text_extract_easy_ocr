from PyQt5.QtWidgets import QTextEdit, QLabel, QApplication, QWidget, QPushButton, QLineEdit, QDesktopWidget, QVBoxLayout
from get_all_json_file_names import ProcessTextFromJsonFiles
from main import AccessUtils
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont, QPixmap
import sys
import os
import json

class OpenInterface(QWidget):

    def __init__(self):
        super().__init__()
        
        self.initUI()

    def openWindow(self):
        # Seta as coordenadas da janela e o titulo
        self.setGeometry(0, 0, 1200, 900)
        self.setWindowTitle('BugHunters System Interface')
        # Centraliza a janela na tela principal
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setTitle(self):
        title_label = QLabel(self)
        title_label.setText("Interface do Sistema")
        title_label.setGeometry(350, 30, 300, 80)
        font = QFont()
        font.setPointSize(16)
        title_label.setFont(font)
        title_label.setAlignment(QtCore.Qt.AlignCenter)

    def resultsLabel(self):
        title_label = QLabel(self)
        title_label.setText("Resultado dos Testes")
        title_label.setGeometry(700, 300, 300, 50)
        font = QFont()
        font.setPointSize(10)
        title_label.setFont(font)
        title_label.setAlignment(QtCore.Qt.AlignCenter)

    def inputLabel(self):
        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 300, 50)
        self.label.setText("Input: ")
        self.label.move(100, 200)
        self.label.resize(300, 30)
    
    def display_image(self):
        self.label = QLabel(self)
        self.label.setGeometry(150, 330, 300, 450)
        #pixmap = QPixmap(path)  # Replace "image.jpg" with the path to your image file
        pixmap = QPixmap("data/7.jpg")
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

    def create_json_display(self):
        json_data = {
            "Image 7": "PASS",
            "Image 13": "PASS",
            "Image 65": "PASS",
            "Image 83": "PASS",
            "Image 100": "PASS"
        }
        json_text = json.dumps(json_data, indent=4)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(700, 350, 300, 300)
        self.text_edit.setPlainText(json_text)
        self.text_edit.setReadOnly(True)

    def initUI(self):
        self.openWindow()
        self.setTitle()
        self.inputLabel()
        # Input directory
        self.input_text = QLineEdit(self)
        self.input_text.setToolTip('Insert your data path')
        self.input_text.move(200, 200)  # Seta posição do campo
        self.input_text.resize(300, 30)  # Seta tamanho do campo
        self.input_text.textChanged.connect(self.enable_start_buttons)
        path = self.input_text.text()
        # Button to start YoLo process
        self.btn_yolo = QPushButton('START YOLO', self)
        self.btn_yolo.move(390, 250)
        self.btn_yolo.setEnabled(False)
        self.btn_yolo.clicked.connect(self.start_yolo_process)
        # Button to start OCR process
        self.btn_ocr = QPushButton('START OCR', self)
        self.btn_ocr.move(100, 250)
        self.btn_ocr.setEnabled(False)
        self.btn_ocr.clicked.connect(self.start_ocr_process)
        # Set background color
        self.setStyleSheet("color: rgb(255,255,255); background-color: rgb(50,50,50);")
        self.display_image()
        self.resultsLabel()
        self.create_json_display()


    def enable_start_buttons(self):
        path = self.input_text.text()
        self.btn_ocr.setEnabled(False)
        self.btn_yolo.setEnabled(False)
        if path == '' or path == ' ':
            self.btn_ocr.setEnabled(False)
            self.btn_yolo.setEnabled(False)
            print("Mandatory field")
        elif path.isnumeric():
            self.btn_ocr.setEnabled(False)
            self.btn_yolo.setEnabled(False)
            print("Invalid path")
        else:
            self.btn_ocr.setToolTip('Click here')
            self.btn_yolo.setToolTip('Click here')
            self.btn_ocr.setEnabled(True)
            self.btn_yolo.setEnabled(True)

    def start_ocr_process(self):
        self.exec_utils = AccessUtils(path)
        self.exec_utils.main(path)

    def start_yolo_process(self):
        path = self.input_text.text()
        self.execute = ProcessTextFromJsonFiles(path)
        print(json.dumps(self.execute.process_text_dict(),indent=4))
       
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = OpenInterface()
    win.show()
    sys.exit(app.exec_())