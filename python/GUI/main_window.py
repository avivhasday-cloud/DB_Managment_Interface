import sys
from enum import IntEnum
from python.GUI.login_page import LoginPage
from python.GUI.main_page_mysql import MainPage
from python.bindings.wrappers.mysql_wrapper import MySQLCWrapper
from PyQt6.QtWidgets import QMainWindow, QApplication, QStackedWidget, QVBoxLayout


class Page(IntEnum):
    LOGIN_PAGE = 0
    MAIN_PAGE = 1


class MainWindowUI(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindowUI, self).__init__(parent)
        self.setGeometry(200, 200, 1200, 700)
        self.login_page_widget = LoginPage()
        self.main_page_widget = MainPage()
        self.stack_widget = QStackedWidget(self)
        self.stack_widget.addWidget(self.login_page_widget)
        self.stack_widget.addWidget(self.main_page_widget)
        self.stack_widget.setCurrentIndex(Page.LOGIN_PAGE)

        layout = QVBoxLayout()
        layout.addWidget(self.stack_widget)
        self.setCentralWidget(self.stack_widget)

        self.init_buttons()
        self.db_wrapper_obj = None

    def init_buttons(self):
        self.login_page_widget.connect_button.clicked.connect(self.on_connect_button_clicked)
        self.main_page_widget.query_button.clicked.connect(self.on_query_button_clicked)
        self.main_page_widget.disconnect_button.clicked.connect(self.on_disconnect_button_clicked)

    def on_connect_button_clicked(self):
        if self.login_page_widget.platform_combo_box.currentText() == "MySQL":
            self.db_wrapper_obj = MySQLCWrapper()
            is_connected_successfully = self.db_wrapper_obj.connect_to_mysql(self.login_page_widget.host.text(),
                                                                             self.login_page_widget.username.text(),
                                                                             self.login_page_widget.password.text(),
                                                                             self.login_page_widget.database.text())
            if is_connected_successfully:
                self.stack_widget.setCurrentIndex(Page.MAIN_PAGE)
                self.login_page_widget.clean_inputs()
                self.main_page_widget.render_db_tree(self.db_wrapper_obj)

    def on_query_button_clicked(self):
        table_dict = self.db_wrapper_obj.get_table_details_by_query(self.main_page_widget.text_edit.toPlainText())
        self.main_page_widget.table_headers = table_dict.get("headers", None)
        self.main_page_widget.table_content = table_dict.get("rows", None)
        self.main_page_widget.render_table_content()

    def on_disconnect_button_clicked(self):
        self.db_wrapper_obj = None
        self.stack_widget.setCurrentIndex(Page.LOGIN_PAGE)


def main():
    app = QApplication(sys.argv)
    win = MainWindowUI()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
