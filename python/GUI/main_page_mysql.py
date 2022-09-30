from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QPushButton, QTextEdit, QTreeView, QTableWidget, QTableWidgetItem, \
    QAbstractItemView
from python.bindings.wrappers.mysql_wrapper import MySQLCWrapper
from python.bindings.utils.parsers import BufferParser


class CustomStandardItem(QStandardItem):
    def __init__(self, item: str):
        super(CustomStandardItem, self).__init__(item)
        self.setEditable(False)


class MainPage(QWidget):
    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)
        uic.loadUi("./ui_files/main_page_mysql.ui", self)
        self.query_button = self.findChild(QPushButton, "queryButton")
        self.disconnect_button = self.findChild(QPushButton, "disconnectButton")
        self.text_edit = self.findChild(QTextEdit, "textEdit")
        self.tree_view = self.findChild(QTreeView, "treeView")
        self.table_widget = self.findChild(QTableWidget, "tableWidget")
        self.tree_view.setHeaderHidden(True)
        self.tree_model = QStandardItemModel()
        self.table_headers = None
        self.table_content = None

    def render_db_tree(self, db_wrapper: any):
        if isinstance(db_wrapper, MySQLCWrapper):
            res = db_wrapper.get_databases()
            for item in res:
                qt_item_obj = CustomStandardItem(item)
                qt_item_obj.setEditable(False)
                buffer, num = db_wrapper.execute_query_and_get_results(f"{MySQLCWrapper.QUERY_TABLES_STATEMENT} {item}")
                res = BufferParser.get_content(buffer, num)
                qt_item_obj.appendRows([CustomStandardItem(sub_item) for sub_item in res])
                self.tree_model.appendRow(qt_item_obj)

        self.tree_view.doubleClicked.connect(lambda index: self.on_click_tree_view_sub_item(index=index, db_wrapper=db_wrapper))
        self.tree_view.setModel(self.tree_model)

    def on_click_tree_view_sub_item(self, index, db_wrapper: MySQLCWrapper):
        item = self.treeView.selectedIndexes()[0]
        selected_item = item.model().itemFromIndex(index)
        parent_text = selected_item.parent().text()
        item_text = item.model().itemFromIndex(index).text()
        table_dict = db_wrapper.get_table_details_by_query(f"SELECT * FROM {parent_text}.{item_text}")
        self.table_headers = table_dict.get("headers", None)
        self.table_content = table_dict.get("rows", None)
        self.render_table_content()

    def render_table_content(self):
        self.table_widget.setRowCount(len(self.table_content))
        self.table_widget.setColumnCount(len(self.table_headers))
        self.table_widget.setHorizontalHeaderLabels(self.table_headers)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        row_index = 0
        col_index = 0
        for row in self.table_content:
            for item in row:
                self.table_widget.setItem(row_index, col_index, QTableWidgetItem(item))
                col_index += 1
            row_index += 1
            col_index = 0
