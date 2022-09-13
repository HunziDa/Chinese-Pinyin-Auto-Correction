from xpinyin import Pinyin
import sqlite3

dbConn=sqlite3.connect("wordData.db")
sql_create="""
    create table wordCount(
        PinYin varchar(20) not null,
        HanZi varchar(20) not null,
        count int not null)
"""
dbConn.execute(sql_create)

p=Pinyin()
rFile=open("sogouw.txt","r",encoding="utf-8")
dataFile=rFile.read()
dataList=dataFile.splitlines()
for line in dataList:
    items=line.split("\t")
    if len(items[0])==2 and int(items[2])>100:
        wordPinyin=p.get_pinyin(items[0],"")
        sql_add=f"insert into wordCount values('{wordPinyin}','{items[0]}','{items[2]}')"
        dbConn.execute(sql_add)
        dbConn.commit()
dbConn.close()
