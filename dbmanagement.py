from sqlite3.dbapi2 import Cursor
import os
import sqlite3
from PyQt5 import QtSql, QtWidgets, Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlTableModel
import pandas as pd
import csv
from pathlib import Path
import sys

savedir = "D:/test/"
dbnamelist = ["CONCEPT","CONCEPT_ANCESTOR", "CONCEPT_CLASS", "CONCEPT_RELATIONSHIP", "CONCEPT_SYNONYM", "VOCABULARY"]
table3_headerlist = ['score','index','concept_id','concept_name','domain_id','vocabulary_id','concept_class_id','standard_concept','concept_code','valid_start_date','valid_end_date','invalid_reason']

    #### DB 생성/교체하는 함수         >>  isinitial 이 필요할 지?? replace 대신 fail / append 옵션 존재
def setDB(dbname,dbpath,isinitial):        
        Path(savedir).mkdir(parents=True, exist_ok=True)
        if os.path.isfile(dbpath):                    
            with sqlite3.connect(savedir + dbname +'.db') as con:
                mydelimiter = setdelimiter(dbpath)
                pdfile = pd.read_csv(dbpath, header=0, low_memory=False, sep= mydelimiter).fillna('')
                if dbname == 'CONCEPT':
                    pdfile.insert(0,'score',0)
            if isinitial:
                ## >> dataframe 안만들고 바로 지정하는 방법 없는지 확인 / 최초생성 시 replace 로?                
                pdfile.to_sql('entire',con, if_exists='replace')                    
                #메인 창에서 index 파일 새로 설정할 떄
            # else:

def addDB():
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(savedir + "CONCEPT.db")
    if not db.open():
        sys.exit(-1)
## db 파일 있는 지 확인하는 함수
def dbexistchk(dbname):
    if os.path.isfile(savedir + dbname + ".db"):
        return True
    else:
        return False 
def filterDBrow(dbname, c_id):
    query = "SELECT * FROM entire WHERE concept_id = '{}'".format(c_id)
    with sqlite3.connect(savedir + dbname +'.db') as con:
        cur = con.cursor()
        cur.execute(query)
        return cur.fetchall()[0]
        
def all_dbexistchk():
    chk = True
    for dbname in dbnamelist:
        if not dbexistchk(dbname):
            chk = False
            break
    return chk

# 특정 db내의 값 가져오는 함수
def getDBvalue(dbname,outcol,targetid):
    query = "SELECT {} FROM entire WHERE concept_id = {}".format(outcol,targetid)
    with sqlite3.connect(savedir + dbname +'.db') as con:
        cur = con.cursor()
        cur.execute(query)
        
        return cur.fetchone()

def searchapprove(dbname,concept_id):
    query = "SELECT EXISTS (SELECT * FROM entire WHERE concept_id ='{}')".format(concept_id)
    with sqlite3.connect(savedir + dbname +'.db') as con:
        cur = con.cursor()
        cur.execute(query)
        return cur.fetchall()[0][0]

def getparent(concept_id):
    query = "SELECT count (*) FROM entire"

def getfilterlist(dbname,rowname):
    query = "SELECT DISTINCT "+rowname+" FROM entire"
    items = []
    # query = "SELECT * FROM entire"
    with sqlite3.connect(savedir + dbname +'.db') as con:
        cur = con.cursor()
        cur.execute(query)
        protolist = cur.fetchall()
        for i in range(len(protolist)):
            items.append(str(protolist[i][0]))
        return items

## csv 파일 delimiter 결정 함수
def setdelimiter(myfile):
    with open(myfile, 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.readline())
        return dialect.delimiter


