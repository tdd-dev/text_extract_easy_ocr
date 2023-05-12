import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QDesktopWidget, QVBoxLayout
from get_all_json_file_names import ProcessTextFromJsonFiles

class OpenInterface(QWidget):

    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):

        # Seta as coordenadas da janela e o titulo
        self.setGeometry(0, 0, 1000, 800)
        self.setWindowTitle('Prototype')
        # Centraliza a janela na tela principal
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # Cria botao com texto
        self.btn = QPushButton('START', self)
        # botao começa desabilitado até inserir o path no input
        self.btn.setEnabled(False)
        # Disparar método on_click quando clicar no botao
        self.btn.clicked.connect(self.start_process_text_from_json)

        # Cria um campo de input editável
        self.input_text = QLineEdit(self)
        self.input_text.setToolTip('Insert your data path')
        self.input_text.move(100, 0)  # Seta posição do campo
        self.input_text.resize(100, 30)  # Seta tamanho do campo

        self.input_text.textChanged.connect(self.enable_start_button)
        

    def enable_start_button(self):
        self.btn.setEnabled(True)
        path = self.input_text.text()
        if path == '' or path == ' ':
            self.btn.setEnabled(False)
            print("Mandatory field")
        elif path.isnumeric():
            self.btn.setEnabled(False)
            print("Invalid path")
        else:
            self.btn.setToolTip('Click here')

    def start_process_text_from_json(self):
        path = self.input_text.text()
        self.execute = ProcessTextFromJsonFiles(path)
        print(self.execute.process_text_dict())

       
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = OpenInterface()
    win.show()
    sys.exit(app.exec_())
