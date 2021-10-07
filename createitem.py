import sys
from PyQt5 import QtPrintSupport
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp, QLabel, QTableWidget, QTableWidgetItem, \
    QFileDialog, QMessageBox
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QImage, QPainter, QIcon, QKeySequence, QIcon, QTextCursor, QCursor, QDropEvent, QTextDocument, \
    QTextTableFormat, QColor 



mod = sys.modules[__name__]
#Qcheckbox 생성
def createQcheckbox(myclass,txt,x,y,ischk):
    setattr(mod,"{}".format(txt+ "_chkbox"), QCheckBox(txt, myclass))
    getattr(mod,"{}".format(txt+ "_chkbox")).setGeometry(x,y,150,20)
    if ischk:
        getattr(mod,"{}".format(txt+ "_chkbox")).setChecked(1)
        # QCheckBox.setChecked
#Qcombobox 생성
def createQcombobox(myclass,txt,x,y,items):
    setattr(mod,"{}".format(txt+ "_combobox"), QComboBox(myclass))
    getattr(mod,"{}".format(txt+ "_combobox")).setGeometry(x,y,150,20)
    getattr(mod,"{}".format(txt+ "_combobox")).addItems(items)
    
# def createqlabel(self, x, y):
#     locals()[self.name + '_label'] = QLabel(self.name, self.myclass)
#     locals()[self.name + '_label'].setGeometry(x, y, 500, 500)
# def createqtable()
