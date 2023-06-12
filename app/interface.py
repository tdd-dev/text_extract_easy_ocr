from PyQt5.QtWidgets import QTextEdit, QLabel, QApplication, QWidget, QPushButton, QLineEdit, QDesktopWidget, QProgressBar,QVBoxLayout
from get_all_json_file_names import ProcessTextFromJsonFiles
from main import AccessUtils
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import sys
import os
import json
from utils.test import ProcessTesting
import time

class OpenInterface(QWidget):

    def __init__(self):
        super().__init__()
        # Command to not allow maximize window
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.path = ""
        
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

    def imagesLabel(self):
        title_label = QLabel(self)
        title_label.setText("Imagens processadas")
        title_label.setGeometry(150, 300, 300, 50)
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
        self.label.setGeometry(150, 350, 300, 450)
        self.exec_utils = AccessUtils(self.path)
        img_list = self.exec_utils.mainImages(self.path)
        for img in img_list:
            pixmap = QPixmap(img)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)
            self.label.show()

    def create_json_display(self,json_data):
        if json_data != {}:
            self.progress_bar.setFormat('Completed')
            self.text_edit.setPlainText(json_data)
            self.progress_bar.setVisible(False)
            self.display_image()

    def start_progress(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(490, 450, 200, 20)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat('Loading... %p%')

        for i in range(101):
            loaded = False
            self.progress_bar.setValue(i)
            time.sleep(0.05)
            QApplication.processEvents()
            if i == 100:
                self.progress_bar.setValue(i)
                QApplication.processEvents()
                loaded = True
            elif i != 100:
                self.progress_bar.setFormat('Loading... %p%')
        if loaded:
            self.progress_bar.setFormat('Ready!')
            QApplication.processEvents()
        return loaded

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
        self.path = self.input_text.text()
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
        # Area to show results after ocr complete the process
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(700, 350, 300, 450)
        self.text_edit.setReadOnly(True)
        self.text_edit.show()
        # Area to show images
        self.img_edit = QTextEdit(self)
        self.img_edit.setGeometry(150, 350, 300, 450)
        self.img_edit.setReadOnly(True)
        self.img_edit.show()
        self.imagesLabel()
        self.resultsLabel()
         # Set background color
        self.setStyleSheet("color: rgb(255,255,255); background-color: rgb(50,50,50);")

    def enable_start_buttons(self):
        self.path = self.input_text.text()
        self.btn_ocr.setEnabled(False)
        self.btn_yolo.setEnabled(False)
        if self.path == '' or self.path == ' ':
            self.btn_ocr.setEnabled(False)
            self.btn_yolo.setEnabled(False)
            print("Mandatory field")
        elif self.path.isnumeric():
            self.btn_ocr.setEnabled(False)
            self.btn_yolo.setEnabled(False)
            print("Invalid path")
        else:
            # self.btn_ocr.setToolTip('Click here')
            # self.btn_yolo.setToolTip('Click here')
            self.btn_ocr.setEnabled(True)
            self.btn_yolo.setEnabled(True)

    def start_ocr_process(self):
        if self.start_progress():
            self.exec_utils = AccessUtils(self.path)
            json_data = self.exec_utils.mainOcr(self.path)
            self.create_json_display(json_data)

    def start_yolo_process(self):
        if self.start_progress():
            self.exec_utils = AccessUtils(self.path)
            self.exec_utils.mainYolo(self.path)
            self.progress_bar.setVisible(False)
            self.display_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = OpenInterface()
    win.show()
    sys.exit(app.exec_())