import os
import sys
from PyQt5.sip import assign
from numpy.core.fromnumeric import size
from numpy.lib.function_base import select
from pyasn1_modules.rfc2459 import Attribute
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp, QLabel, QTableWidget, QTableWidgetItem, \
    QFileDialog, QMessageBox
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QCloseEvent, QImage, QPainter, QIcon, QKeySequence, QIcon, QTextCursor, QCursor, QDropEvent, QTextDocument, \
    QTextTableFormat, QColor 
from PyQt5 import QtPrintSupport
from numpy.core.numeric import indices
import openpyxl
from googletrans import Translator
import csv
import pandas as pd
import sqlite3
from pathlib import Path
from numpy import dot
from numpy.linalg import norm
import numpy as np
from pandas.core.frame import DataFrame
from pandas.core.indexes.base import Index
from pandas.core.indexes.range import RangeIndex
from pandas.io.pytables import IndexCol
from requests.models import CaseInsensitiveDict
from createitem import *
from dbmanagement import *
from medtranslate import *

#코사인 유사도 사용 용도 import => 안됨
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#@@@@@@@@@@@@@@@@@@@@########### 최초 인덱스 설정 화면#####################################################################################################
class Setindex(QMainWindow):
    ## 저장할 기본 경로 및 필수 파일이름 - 경로는 사용자가 선택하게 변경 기능 추가?
    
    def initUI(self):
        self.setWindowTitle('Rebuild index')
        self.setWindowIcon(QIcon('wolf.jpg'))
        self.setGeometry(300, 300, 300, 200)

        Setindex.indextext = QTextEdit(self)
        selectfile_btn = QPushButton(self)
        Setindex.indextext.setText('')
        selectfile_btn.setText('pick file')

        buildbtn = QPushButton(self)
        buildbtn.setText('Build index')

#####  >>> indextext 수정불가로 지정& 한줄로 변경
        Setindex.indextext.setGeometry(0, 0, 200, 50)
        selectfile_btn.setGeometry(220, 0, 100, 50)
        buildbtn.setGeometry(100, 100, 100, 60)

        selectfile_btn.clicked.connect(self.setdir)
        buildbtn.clicked.connect(self.firstset)
        self.show()

######## index설정창 닫고 메인 창 실행 함수  >> 메인 창에서 index 새로 설정할 수 있게 추가필요
    def openMyApp(self):
        self.myapp = MyApp()
        self.myapp.show()
        self.close()

    ## 기본
    def __init__(self):
        super().__init__()
        if all_dbexistchk():
            self.openMyApp()
        else:
            self.initUI()
            
    ## db csv파일 저장된 폴더 지정 함수
    def setdir(self):
        Setindex.indexdir = QFileDialog.getExistingDirectory(self.window(), "Select Dir")
        Setindex.indextext.setText(Setindex.indexdir)

    ## 최초 db 확인 및 생성
    def firstset(self):
        for dbname in dbnamelist:
            # db파일도 없고 해당경로에 csv 파일도 없으면
            if not (dbexistchk(dbname) or os.path.isfile(Setindex.indexdir + "/" + dbname +".csv")) == True:
                QtWidgets.QMessageBox.warning(self, "QMessageBox", dbname +".csv file is neeeded")                
            elif dbexistchk(dbname) == False:
                setDB(dbname,Setindex.indexdir + "/" + dbname +".csv",True)
        if all_dbexistchk():
            self.openMyApp()


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@############메인 화면#################################################################################
class MyApp(QMainWindow):
    filename = mrow = mcolumn = db = dbheader = ''
    mod = sys.modules[__name__]

    ## 생성자
    def __init__(self):
        super().__init__()
        self.initUI()

    ## 파일오픈 함수 설정

    def fileopen(self):
        try:
            MyApp.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            MyApp.filetype = QFileInfo(MyApp.filename[0]).completeSuffix()

            if (MyApp.filetype == ('xlsx' or 'xls')):
                MyApp.df = pd.read_excel(MyApp.filename[0],header=None).fillna('')
            elif MyApp.filetype == 'csv':
                MyApp.df = pd.read_csv(MyApp.filename[0],header=None, low_memory=False).fillna('')
            else:
                QtWidgets.QMessageBox.warning(self, "QMessageBox", "excel or csv file is neeeded")
                return False

            MyApp.mcolumn = len(MyApp.df.columns)
            MyApp.mrow = len(MyApp.df)
            MyApp.dbheader = list(map(str,MyApp.df.values.tolist()[0])) 
            self.setwindow = Setcolumnwindow()
            self.setwindow.show()
        except:
            return False
    
    ## 테이블에 해당 값 저장 함수
    def set_synonym2(self):
        try:
            self.tx = str(MyApp.table3.selectedIndexes()[1].data())
            if self.tx != '':       
                reply = QtWidgets.QMessageBox.question(self,'Message','Are you sure you want to change?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    syn_item = MyApp.tableWidget.selectedItems()[4]
                    MyApp.df.iloc[syn_item.row(),Setcolumnwindow.conceptIDrownum] = self.tx
                    MyApp.tableWidget.setItem(syn_item.row(),syn_item.column(),QTableWidgetItem(self.tx))

                    Setcolumnwindow.setdata_from_ID(self,MyApp.tableWidget.selectedItems()[4].row(),MyApp.table3.selectedIndexes()[1].data(),True)              
                else:
                    
                    return False
        except:
            return False
            
    def set_synonym(self):
        try:
            self.tx = str(MyApp.table3.selectedIndexes()[1].data())
            indexs = MyApp.tableWidget.selectedIndexes()
            indexlist = []
            for index in indexs:
                indexlist.append(index.row())
            indexlist = set(indexlist)
            print(indexlist)
            if indexlist != []:  
                reply = QtWidgets.QMessageBox.question(self,'Message','Are you sure you want to change?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    for index in indexlist:
                        MyApp.df.iloc[index,Setcolumnwindow.conceptIDrownum] = self.tx
                        MyApp.tableWidget.setItem(index,5,QTableWidgetItem(self.tx))
                        Setcolumnwindow.setdata_from_ID(self,index,MyApp.table3.selectedIndexes()[1].data(),True)
                else:
                    
                    return False
        except:
            return False


    ## 창 닫을 때 확인 함수
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    ####score 테이블 데이터 적용 함수(알고리즘 포함)
    def set_scoretableview(self):
        try:
            view = MyApp.table3
            view.setModel(MyApp.table3Model(self))
            view.setSortingEnabled(True)
            view.sortByColumn(1,Qt.SortOrder.DescendingOrder)
            view.hideColumn(0)
        except(AttributeError):
            return False
    def get_score(scoremode,word1,word2):
        word1 = str(word1).lower()
        word2 = str(word2).lower()
        if scoremode == 'Jaccard':
            union = set(word1).union(set(word2))
            intersection = set(word1).intersection(set(word2))
            score = round(len(intersection) / len(union),4)

        elif scoremode == 'Jaccard2':
            word1 = word1.split()
            word2 = word2.split()
            union = set(word1).union(set(word2))
            intersection = set(word1).intersection(set(word2))
            score = str(round(len(intersection) / len(union),4))

        elif scoremode == 'Cosine':
            #코사인 유사도 알고리즘 점수 구현 함수    
                # tfidf = TfidfVectorizer(stop_words=None)
                # tfidf_matrix = tfidf.fit_transform(MyApp.proxymodel)
                # cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
                # idx = indices[word1]
                # score = list(enumerate(cosine_sim[idx]))
                score = 0


        return score     

    
##############################################################################csv로 저장 코드 더하기

    def writeCsv(self,mode):
        # savedir = QtWidgets.QFileDialog.getExistingDirectory(self,'select directory')
        path = QFileDialog.getSaveFileName(self, 'Save File', MyApp.filename[0], "CSV Files(*.csv *.txt)")
        #path = QFileDialog.getSaveFileName(self, 'Save File', QDir.homePath() + "/export.csv", "CSV Files(*.csv *.txt)")
   
        if mode == 'w':
            if MyApp.tableWidget.rowCount() != 0:
                MyApp.df.to_csv(path[0],index=False,header = False, mode='w')
        
    #### 인쇄, 인쇄미리보기
    def handlePrint(self):
        if self.tableWidget.rowCount() == 0:
            self.msg("no rows")
        else:
            dialog = QtPrintSupport.QPrintDialog()
            if dialog.exec_() == QDialog.Accepted:
                self.handlePaintRequest(dialog.printer())
                self.msg("Document printed")

    def handlePreview(self):
        if MyApp.tableWidget.rowCount() == 0:
            self.msg("no rows")
        else:
            dialog = QtPrintSupport.QPrintPreviewDialog()
            dialog.setFixedSize(1000, 700)
            dialog.paintRequested.connect(self.handlePaintRequest)
            dialog.exec_()
            self.msg("Print Preview closed")

    def handlePaintRequest(self, printer):
        # find empty cells
        for row in range(MyApp.tableWidget.rowCount()):
            for column in range(MyApp.tableWidget.columnCount()):
                myitem = MyApp.tableWidget.item(row, column)
                if myitem is None:
                    item = QTableWidgetItem("")
                    MyApp.tableWidget.setItem(row, column, item)
        printer.setDocName(MyApp.filename[0])
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = MyApp.tableWidget.model()
        tableFormat = QTextTableFormat()
        tableFormat.setBorder(0.2)
        tableFormat.setBorderStyle(3)
        tableFormat.setCellSpacing(0)
        tableFormat.setTopMargin(0)
        tableFormat.setCellPadding(4)
        table = cursor.insertTable(model.rowCount(), model.columnCount(), tableFormat)
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(MyApp.tableWidget.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def filter_item(self,tablename,textvalue):  
        try:
            for col in range(tablename.rowCount()):
                tablename.setRowHidden(col,False)
            if textvalue.text():
                items = tablename.findItems(textvalue.text(),QtCore.Qt.MatchContains)
                itemrowlist = []
                for item in items:
                    itemrowlist.append(item.row())
                for col in range(tablename.rowCount()):
                    if col not in itemrowlist:
                        tablename.setRowHidden(col,True)
        except(AttributeError):
            return False
    # 하단에 메세지 표시
    def msg(self, message):
        self.statusBar().showMessage(message)


    # # cloud 없이 번역
    def translate_item(self,tableitem):
        trans = Translator()
        result = trans.translate(tableitem ,dest='en')
        return result.text


    #### 선택한 행에 포함된 값 다른 테이블에 입력         
    def settable2(self):
        try:    
            items = MyApp.tableWidget.selectedItems()
                
            MyApp.table2.setItem(0,0,QTableWidgetItem(items[1].text()))
            MyApp.table2.setItem(0,1,QTableWidgetItem(items[2].text()))
            MyApp.table2.setItem(0,2,QTableWidgetItem(items[3].text())) 
            MyApp.table2.setItem(0,3,QTableWidgetItem(self.translate_item(items[2].text())))
            # MyApp.table2.setItem(0,3,QTableWidgetItem(translate_word_with_glossary(items[2].text(),project_id,glossary_id)))
            MyApp.table3.reset()

        except IndexError or AttributeError:
            return False
    
        #table3 최초 설정
    def set_table3(self):
        model = QSqlTableModel()
        model.insertColumns(0,12)
        for i in range(len(table3_headerlist)):
            model.setHeaderData(i,Qt.Orientation.Horizontal,table3_headerlist[i])    
        self.table3.setModel(model)
        self.table3.setGeometry(5,420,1190,400)
        self.table3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table3.verticalHeader().setVisible(False)
        self.table3.setSelectionBehavior(QAbstractItemView.SelectRows)



    # 데이터 필터 적용쿼리
    def getfilterquery():
        query = ""
        isfirst = True
        if getattr(mod,"conceptclass_chkbox").isChecked():
            query += "concept_class_id = '" + str(getattr(mod,"conceptclass_combobox").currentText()) + "'"
            isfirst = False
        if getattr(mod,"standard_concept_chkbox").isChecked():
            if not isfirst:
                query += " and "
            query += "standard_concept = '" + str(getattr(mod,"standard_concept_combobox").currentText()) + "'"
            isfirst = False
        if getattr(mod,"vocabulary_chkbox").isChecked():
            if not isfirst:
                query += " and "
            query += "vocabulary_id = '" + str(getattr(mod,"vocabulary_combobox").currentText()) + "'"
            isfirst = False
        if getattr(mod,"domain_chkbox").isChecked():
            if not isfirst:
                query += " and "
            query += "domain_id = '" + str(getattr(mod,"domain_combobox").currentText()) + "'"
        
        return query

    def table3Model(self):
        model = QSqlTableModel()
        model.setTable("entire")
        model.setFilter(MyApp.getfilterquery())
        model.select()
        while model.canFetchMore():
            model.fetchMore()
        currentalgorithm = str(getattr(mod,"chk_algorithm_combobox").currentText())
        word2 = MyApp.table2.item(0,3).text()
        for i in range(model.rowCount()):
            word1 = model.data(model.index(i,3))
            model.setData(model.index(i,1),MyApp.get_score(currentalgorithm,word1,word2))
            model.submit()
        model.sort(1,Qt.SortOrder.DescendingOrder)
        MyApp.proxymodel = QSortFilterProxyModel()
        MyApp.proxymodel.setSourceModel(model)
        # MyApp.proxymodel.sort(1,Qt.SortOrder.DescendingOrder)

        return MyApp.proxymodel
    
    def setcomment(self):
        indexs = MyApp.tableWidget.selectedIndexes()
        indexlist = []
        for index in indexs:
            indexlist.append(index.row())
        indexlist = set(indexlist)
        self.setcomment = Setpopupwindow("comment",indexlist)        
        self.setcomment.show()

    def table3Model2(self):
        currentalgorithm = str(getattr(mod,"chk_algorithm_combobox").currentText())
        query = "SELECT  * FROM entire WHERE (" + MyApp.getfilterquery() + ")"
        word2 = MyApp.table2.item(0,3).text()
        
        # query2 = "UPDATE entire SET score = "
        with sqlite3.connect("D:/test/CONCEPT.db") as con:
            cur = con.cursor()
            cur.execute(query)
            records = cur.fetchall()
            for row in records:
                word1 = str(row[3])
                score = str(MyApp.get_score(currentalgorithm,word1,word2))
                cur.execute("UPDATE entire SET score = '" + score + "' WHERE concept_id = '" + str(row[2]) + "'")

        
        model = QSqlTableModel()
        model.setTable("entire")
        model.select()
        MyApp.proxymodel = QSortFilterProxyModel()
        MyApp.proxymodel.setSourceModel(model)
        
        return model

    ############## 윈도우창 관련 설정
    def initUI(self):
        self.setWindowTitle('My First Application')
        self.setWindowIcon(QIcon('wolf.jpg'))
        self.setGeometry(100, 100, 1200, 900)
        self.statusBar().showMessage('ready')
 
        ## 하위 메뉴 세부 설정
        importAction = QAction(QIcon(), 'import', self)
        importAction.setShortcut('Ctrl + I')
        importAction.setStatusTip('import file')
        importAction.triggered.connect(self.fileopen)

        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+W')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(lambda:self.close())

        saveAction = QAction(QIcon(), 'Save', self)
        saveAction.setShortcut('Ctrl + S')
        saveAction.setStatusTip('Save file')
        saveAction.triggered.connect(lambda:self.writeCsv('w'))
        
        assignAction = QAction(QIcon(), 'Assign reviewers', self)
        assignAction.setShortcut('Ctrl + A')
        assignAction.setStatusTip('Assign reviewers')
        assignAction.triggered.connect(self.openSetreviewer)

        ## 메뉴바 및 하위 메뉴 생성
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu2 = menubar.addMenu('&Edit')
        filemenu3 = menubar.addMenu('&View')
        filemenu4 = menubar.addMenu('&Help')
        filemenu.addAction(importAction)
        filemenu.addAction(saveAction)
        filemenu.addAction(exitAction)
        filemenu.addAction(QIcon.fromTheme("document-print-preview"), "Print Preview", self.handlePreview,
                           "Shift+Ctrl+P")
        filemenu.addAction(QIcon.fromTheme("document-print"), "Print", self.handlePrint, QKeySequence.Print)
        filemenu2.addAction(assignAction)

        ## 테이블1 최초 설정
        MyApp.tableWidget = QTableWidget(self)
        MyApp.tableWidget.setGeometry(5, 50, 1195, 200)
        MyApp.tableWidget.setRowCount(0)
        MyApp.tableWidget.setColumnCount(18)
        MyApp.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        MyApp.tableWidget.verticalHeader().setVisible(False)
        MyApp.tableWidget.cellChanged
        MyApp.column_headers = ['Status', 'Source code', 'Source term', 'Frequency', 'Match score', 'Concept ID',
                          'Concept name', 'Domain', 'Vocabulary', 'Concept class', 'Standard concept', 'Concept code',
                          'Parents', 'Children', 'Assigned To', 'Equivalence', 'Comment', 'Status Provenance']
        MyApp.tableWidget.setHorizontalHeaderLabels(MyApp.column_headers)
        MyApp.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        MyApp.tableWidget.setSortingEnabled(True)
        MyApp.tableWidget.itemSelectionChanged.connect(self.settable2)
        MyApp.tableWidget.doubleClicked.connect(self.setcomment)
        MyApp.tableWidget.itemSelectionChanged.connect(self.set_table3)

        MyApp.filtertxt = QLineEdit(self)
        MyApp.filtertxt.setGeometry(800,20,200,30)
        MyApp.filtertxt.returnPressed.connect(lambda: self.filter_item(MyApp.tableWidget,MyApp.filtertxt))
        self.filterbtn = QPushButton('filter',self)
        self.filterbtn.setGeometry(1010,20,100,30)
        self.filterbtn.clicked.connect(lambda: self.filter_item(MyApp.tableWidget,MyApp.filtertxt))

        ## 테이블2 최초 설정
        MyApp.label1 = QLabel('Source Code', self)
        MyApp.label1.setGeometry(5, 250, 100, 20)
        MyApp.table2 = QTableWidget(self)
        MyApp.table2.setGeometry(5, 290, 580, 80)
        MyApp.table2.setRowCount(1)
        MyApp.table2.setColumnCount(4)
        MyApp.table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        MyApp.table2.verticalHeader().setVisible(False)
        # table2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode)
        MyApp.table2.horizontalHeader().cascadingSectionResizes
        column_headers2 = ['Source code', 'Source term', 'Frequency','translate']
        MyApp.table2.setHorizontalHeaderLabels(column_headers2)
        MyApp.table2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        MyApp.table2.setSelectionBehavior(QAbstractItemView.SelectRows)
        MyApp.table2.setSortingEnabled(True)
        MyApp.table2.resizeColumnsToContents()
        MyApp.table2.horizontalHeader().setStretchLastSection(True)

        conecp_class_items = getfilterlist("concept","concept_class_id")
        voca_items = getfilterlist('concept','vocabulary_id')
        domain_items = getfilterlist('concept', 'domain_id')
        standard_concept_items = getfilterlist('concept', 'standard_concept')
        score_items = ['Jaccard','Jaccard2','Cosine']
        createQcheckbox(self,'standard_concept',600,330,True)
        createQcheckbox(self,'conceptclass',920,300,False)
        createQcheckbox(self,'vocabulary',920,330,False)
        createQcheckbox(self,'domain',920,360,False)
        createQcombobox(self,'standard_concept',750,330,standard_concept_items)
        createQcombobox(self,'conceptclass',1020,300,conecp_class_items)
        createQcombobox(self,'vocabulary',1020,330,voca_items)
        createQcombobox(self,'domain',1020,360,domain_items)
        createQcombobox(self,'chk_algorithm',750,300,score_items)


        
        # # 테이블3 최초설정
        MyApp.table3 = QtWidgets.QTableView(self)
        self.set_table3()
        addDB()
        
        MyApp.searchbtn = QPushButton(self)
        MyApp.searchbtn.setText('Search')
        MyApp.searchbtn.setGeometry(700,840,80,40)
        MyApp.searchbtn.clicked.connect(MyApp.set_scoretableview)
        MyApp.setbtn = QPushButton(self)
        MyApp.setbtn.setText('Set Synonym')
        MyApp.setbtn.setGeometry(800,840,100,40)
        MyApp.setbtn.clicked.connect(self.set_synonym)

        MyApp.filtertxt2 = QLineEdit(self)
        MyApp.filtertxt2.setGeometry(115,375,200,30)
        MyApp.filtertxt2.textChanged.connect(lambda: self.filter_data(MyApp.filtertxt2.text()))
        
        self.filterlabel = QLabel('filter',self)
        self.filterlabel.setGeometry(15,375,100,30)
        self.show()

    # def setassign(self):

    def filter_data(self,word):
        try:
            regExp = QRegExp(word)
            regExp.setPatternSyntax(QRegExp.Wildcard)
            regExp.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

            # MyApp.proxymodel.setFilterCaseSensitivity(Qt.CaseSensitivity(1))
            MyApp.proxymodel.setFilterRegExp(regExp)
            MyApp.proxymodel.setFilterKeyColumn(-1)
            view = MyApp.table3
            view.setModel(MyApp.proxymodel) 
            view.setSortingEnabled(True)
            view.sortByColumn(1,Qt.SortOrder.DescendingOrder)
            view.hideColumn(0)
        except(AttributeError):
            return False

    def openSetreviewer(self):
        indexs = MyApp.tableWidget.selectedIndexes()
            
        indexlist = []
        for index in indexs:
            indexlist.append(index.row())
        indexlist = set(indexlist)
    
        if indexlist == []:
            QtWidgets.QMessageBox.warning(self, "QMessageBox", "selected rows are neeeded")
        else:
        # 바로 쓰면 창이 바로 꺼짐
            self.setreviewers = Setpopupwindow("reviewer",*indexlist)        
            self.setreviewers.show()
        
class Setpopupwindow(QMainWindow):

    def __init__(self,popup_type,*selectedrows):
        super().__init__()
        self.popup_type = popup_type
        self.selectedrows = selectedrows
        # self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.initUI()    

    def initUI(self):
        self.setGeometry(300, 300, 270, 100)
        Setpopupwindow.indextext = QTextEdit(self)
        Setpopupwindow.assign_btn = QPushButton(self)
        Setpopupwindow.indextext.setText(' ')
        Setpopupwindow.assign_btn.setText('assign')

        self.reviewerlabel = QLabel(self)
        if self.popup_type == "reviewer":
            self.setWindowTitle('Assign reviewer')
            self.reviewerlabel.setText('Reviewers : ')
            col = 14
        elif self.popup_type == "comment":
            self.setWindowTitle('Set comment')
            self.reviewerlabel.setText('Comment : ')
            col = 16
        self.reviewerlabel.setGeometry(10,10,70,20)
        Setpopupwindow.indextext.setGeometry(100, 10, 150, 30)
        Setpopupwindow.assign_btn.setGeometry(210, 60, 50, 30)
        Setpopupwindow.assign_btn.clicked.connect(lambda: self.change_reviewers(col,self.selectedrows))
        self.show()

    def change_reviewers(self,col,rows):
        print(rows)
        for row in rows:
            MyApp.tableWidget.setItem(row,col,QTableWidgetItem(Setpopupwindow.indextext.toPlainText()))
        self.close()


## import한 파일 컬럼 설정 ##
class Setcolumnwindow(QMainWindow):
    #coderow = namerow = frequencyrow = conceptIDrow = additionalrow = 0

       ## 기본
    def __init__(self):
        super().__init__()
        self.initUI()    
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
    
    def initUI(self):
        self.setWindowTitle('Set column')
        self.setWindowIcon(QIcon('wolf.jpg'))
        self.setGeometry(300, 300, 700, 600)
        
        self.firsttable = QTableWidget(self)
        self.firsttable.setGeometry(5,30,650,300)
        self.firsttable.setColumnCount(MyApp.mcolumn)
        self.firsttable.setRowCount(MyApp.mrow-1)
        self.firsttable.setHorizontalHeaderLabels(MyApp.dbheader)
        self.firsttable.verticalHeader().setVisible(False)
        self.firsttable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.firsttable.setSelectionBehavior(QAbstractItemView.SelectRows)

        stylesheet = "::section{Background-color:rgb(153,153,153)}"
        self.firsttable.horizontalHeader().setStyleSheet(stylesheet)
        # self.firsttable.itemSelectionChanged.connect(self.print_row)
        # combolist = [''] + MyApp.dbheader

        boxheaderlist = ['Source code column', 'Source name column', 'Source frequency column', 'Auto concept ID column', 'Additional info column']
        for i in range(5):
            globals()['boxlabel{}'.format(i)] = QLabel(self)
            globals()['boxlabel{}'.format(i)].setGeometry(5, 350+i*30, 150, 20)
            globals()['boxlabel{}'.format(i)].setText(boxheaderlist[i])
            globals()['headerbox{}'.format(i)] = QComboBox(self)
            globals()['headerbox{}'.format(i)].setGeometry(180,350+i*30, 150, 20)
            globals()['headerbox{}'.format(i)].addItems(MyApp.dbheader)

        self.importbtn = QPushButton(self)
        self.importbtn.setGeometry(600,500,70,50)
        self.importbtn.setText('import')
        self.importbtn.clicked.connect(self.sortdata)

        ### 기본 셀 값 입력

        for c in range(MyApp.mcolumn):
            for r in range(MyApp.mrow-1):
                self.firsttable.setItem(r,c,QTableWidgetItem(str(MyApp.df.iloc[r+1, c])))
        # else:
        #     for c in range(MyApp.mcolumn):
        #         for r in range(MyApp.mrow-1):
        #             self.firsttable.setItem(r,c,QTableWidgetItem(str(MyApp.db[c][r])))


    #### 선택한 열을 결과 테이블 특정 열에 입력
    def sortdata(self):
        Setcolumnwindow.coderownum = globals()['headerbox0'].currentIndex()
        Setcolumnwindow.namerownum = globals()['headerbox1'].currentIndex()
        Setcolumnwindow.frequencyrownum = globals()['headerbox2'].currentIndex()
        Setcolumnwindow.conceptIDrownum = globals()['headerbox3'].currentIndex()
        #### 기존 row외의 row 추가 -이후에 ########
        # Setcolumnwindow.additionalrownum = globals()['headerbox4'].currentIndex()
        #Setcolumnwindow.setcolumnnum = 0

        MyApp.tableWidget.clear()
        MyApp.tableWidget.setHorizontalHeaderLabels(MyApp.column_headers)
        MyApp.tableWidget.setRowCount(MyApp.mrow-1)
        templist = [Setcolumnwindow.coderownum, Setcolumnwindow.namerownum, Setcolumnwindow.frequencyrownum, Setcolumnwindow.conceptIDrownum]
        # templist = [Setcolumnwindow.coderownum, Setcolumnwindow.namerownum, Setcolumnwindow.frequencyrownum, Setcolumnwindow.conceptIDrownum, Setcolumnwindow.additionalrownum]
        column_num_list = [1,2,3,5,6]


        for num in range(len(templist)):
            for r in range(MyApp.mrow-1):
                MyApp.tableWidget.setItem(r,column_num_list[num],QTableWidgetItem(str(MyApp.df.iat[(r+1,templist[num])])))
                if column_num_list[num] ==5:
                    c_id = MyApp.tableWidget.item(r,5).text()
                    if searchapprove('concept',c_id) == 1:
                        self.setdata_from_ID(r,c_id,True)
                    else:
                        self.setdata_from_ID(r,c_id,False)
        self.close()

    #approve 설정 함수        
    def setdata_from_ID(self,row,c_id,bool):
        if bool:
            line = filterDBrow('concept',c_id)
            MyApp.tableWidget.setItem(row,0,QTableWidgetItem("approve"))        
            for i in range(7):
                MyApp.tableWidget.setItem(row,i+5,QTableWidgetItem(str(line[i+2])))
        else:
            MyApp.tableWidget.setItem(row, 0, QTableWidgetItem("unapprove"))

            


## 실행부
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Setindex()
    sys.exit(app.exec_())
