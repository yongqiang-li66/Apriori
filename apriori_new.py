import numpy as np
import pandas as pd
# def loadDataSet():
#     dataSet = [line.split() for line in open('mushroom.dat').readline()]
#     return dataSet
# dataSet = loadDataSet()
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        #print(transaction)
        for item in transaction:
            #print(item)
            if not [item] in C1:
                #print([item])
                C1.append([item])
                #print(C1)
    C1.sort()
    #print(C1)
    return list(map(frozenset,C1))
#createC1(dataSet)

def scanD(D,CK,minSupport):
    ssCnt = {}
    for tid in D:
        for can in CK:
            if can.issubset(tid):
                if not can in ssCnt:ssCnt[can]=1
                else:ssCnt[can]+=1
    numItems = float(len(D))
    retList = []
    supportData={}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support>=minSupport:
            retList.insert(0,key)
        supportData[key]=support
    # print(retList)
    # print(supportData)
    return retList,supportData
# C1=createC1(dataSet)
# scanD(dataSet,C1,0.5)
#频繁项集两两组合
def aprioriGen(Lk,k):
    retList=[]
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1=list(Lk[i])[:k-2];L2=list(Lk[j])[:k-2]
            L1.sort();L2.sort()
            if L1==L2:
                retList.append(Lk[i]|Lk[j])
    return retList
def apriori(dataSet,minSupport=0.3):
    C1=createC1(dataSet)
    D=list(map(set,dataSet))
    L1,supportData =scanD(D,C1,minSupport)
    L=[L1]
    k=2
    while(len(L[k-2])>0):
        CK = aprioriGen(L[k-2],k)
        Lk,supK = scanD(D,CK,minSupport)
        supportData.update(supK)
        L.append(Lk)
        k+=1
    return L,supportData
#规则计算的主函数
def generateRules(L,supportData,minConf=0.7):
    bigRuleList = []
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if(i>1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
    return bigRuleList


def calcConf(freqSet,H,supportData,brl,minConf=0.7):
    prunedH=[]
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf>=minConf:
            print (freqSet-conseq,'--->',conseq,'conf:',conf)
            brl.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH
def rulesFromConseq(freqSet,H,supportData,brl,minConf=0.7):
    m = len(H[0])
    if (len(freqSet)>(m+1)):
        Hmp1 = aprioriGen(H,m+1)
        Hmp1 = calcConf(freqSet,Hmp1,supportData,brl,minConf)
        if(len(Hmp1)>1):
            rulesFromConseq(freqSet,Hmp1,supportData,brl,minConf)


# def Read_list(filename):
#     file1 = open(filename+".txt", "r")
#     list_row =file1.readlines()
#     list_source = []
#     for i in range(len(list_row)):
#         column_list = list_row[i].strip().split("\t")  # 每一行split后是一个列表
#         list_source.append(column_list)                # 在末尾追加到list_source
#     file1.close()
#     return list_source
# dataSet=Read_list('mushroom')

# dataSet=pd.read_table('mushroom.txt',header=None,sep=' ')
# d = dataSet.values
# y = {2.0}
# L,supportData=apriori(d,minSupport=0.3)
# print(L[1])
# for item in L[1]:
#     if item.intersection(y):
#         print(item) #查看与特征值2相交的item

if __name__ == '__main__':
    dataSet = pd.read_table('mushroom.txt', header=None, sep=' ')
    d = dataSet.values
    y = {2.0}
    L,supportData=apriori(d,minSupport=0.3)
    for item in L[1]:
        if item.intersection(y):
            print(item)  # 查看与特征值2相交的item
    # rules = generateRules(L, supportData, minConf=0.7)