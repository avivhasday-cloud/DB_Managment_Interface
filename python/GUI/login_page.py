from PyQt6.QtWidgets import  QWidget, QApplication, QLineEdit, QComboBox, QPushButton
import sys
from PyQt6 import uic

login_ui_file_path = "ui_files/login_page.ui"


class LoginPage(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        uic.loadUi(login_ui_file_path, self)
        # Define widgets of login page
        self.host = self.findChild(QLineEdit, "hostLineEdit")
        self.username = self.findChild(QLineEdit, "userNameLineEdit")
        self.password = self.findChild(QLineEdit, "passwordLineEdit")
        self.database = self.findChild(QLineEdit, "databaseLineEdit")
        self.platform_combo_box = self.findChild(QComboBox, "platformComboBox")
        self.connect_button = self.findChild(QPushButton, "pushButton")

    def clean_inputs(self):
        for widget in self.findChildren(QLineEdit):
            widget.clear()


