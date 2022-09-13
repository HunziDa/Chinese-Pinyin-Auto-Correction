from cmath import log10
import sqlite3

def minimumEditDistance(target,candidate):
    len_1=len(target)
    len_2=len(candidate)
    dis_matrix=[ [0] * (len_1+1) for i in range(len_2+1)]
    for i in range(0,len_1+1):
        dis_matrix[0][i]=i
    for i in range(0,len_2+1):
        dis_matrix[i][0]=i
    
    for i in range(1,len_2+1):
        for j in range(1,len_1+1):
            if(candidate[i-1]==target[j-1]):flag=0
            else:flag=1
            dis_matrix[i][j]=min(dis_matrix[i-1][j]+1,dis_matrix[i][j-1]+1,dis_matrix[i-1][j-1]+flag)
    return dis_matrix[len_2][len_1]
def differ(str_1,str_2):
    n=min(len(str_1),len(str_2))
    flag=-1
    for i in range(0,n):
        if(str_1[i]!=str_2[i]):
            flag=i
            break
    return flag

def autoCorrection(target,flag_neighboringIncluded):
    oneMistakeList=[]
    twoMistakeList=[]
    candidateList=[target]
    finalResult=[]
    confuseSet={
        "h":["f"],
        "f":["h"],
        "l":["n"],
        "n":["l","ng"],
        "ng":["n"],
        "z":["zh"],
        "c":["ch"],
        "s":["sh"],
        "zh":["z"],
        "ch":["c"],
        "sh":["s"],
    }
    confuseSet_neighboringIncluded={
        "h":["f","u"],
        "f":["h","e"],
        "l":["n","o","i"],
        "n":["l","ng"],
        "ng":["n"],
        "z":["zh","a"],
        "c":["ch"],
        "s":["sh","a"],
        "zh":["z"],
        "ch":["c"],
        "sh":["s"],
        "a":["q","w","s","x","z"],
        "e":["w","s","d","f","r"],
        "i":["u","j","k","l","o"],
        "o":["i","k","l","p"],
        "u":["y","h","j","k","i"],
        "y":["u"],
        "j":["u","i"],
        "k":["u","i","o"],
        "l":["i","o"],
        "p":["o"],
        "q":["a"],
        "w":["a","e"],
        "d":["e"],
        "r":["e"],
    }
    if flag_neighboringIncluded==1:
        confuseSet=confuseSet_neighboringIncluded

    for pairs in confuseSet:
        if pairs in target:
            for item in confuseSet[pairs]:
                tmp=target.replace(pairs,item,1)
                oneMistakeList.append(tmp)
                for pairs in confuseSet:
                    if tmp.find(pairs,differ(tmp,target)+1):
                        for item in confuseSet[pairs]:
                            tmp2=target[differ(tmp,target):]
                            tmp2=tmp2.replace(pairs,item,1)
                            tmp2=target[0:differ(tmp,target)]+tmp2
                            #print(tmp2)
                            oneMistakeList.append(tmp2)

    for phrase in oneMistakeList:
        twoMistakeList.append(phrase)
        for pairs in confuseSet:
            if phrase.find(pairs,differ(phrase,target)+1):
                for item in confuseSet[pairs]:
                    tmp=phrase[differ(phrase,target):]
                    tmp=tmp.replace(pairs,item,1)
                    tmp=phrase[0:differ(phrase,target)]+tmp
                    #print(tmp)
                    twoMistakeList.append(tmp)
    for item in twoMistakeList:
        if item not in candidateList:
            candidateList.append(item)

    dbConn=sqlite3.connect("wordData.db")
    sum=251909774405

    for candidate in candidateList:
        sql_find=f"select * from wordCount where PinYin='{candidate}'"
        res=dbConn.execute(sql_find)
        res=res.fetchall()
        if len(res)>0: 
            for item in res:
                rate=round((float(item[2])/sum)*100000,5)
                editDis=minimumEditDistance(target,candidate)
                tmp=[item[1],candidate,rate,editDis,pow(10,2-editDis)+rate]
                finalResult.append(tmp)
    dbConn.close()
    finalResult.sort(key=lambda x:x[4],reverse=True)
    for item in finalResult:
        print(item[0],item[1],item[4])
        
target="wrnnuan"
flag_neighboringIncluded=1
autoCorrection(target,flag_neighboringIncluded)