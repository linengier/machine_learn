#!/usr/bin/python  
#-*- coding:utf-8 -*-  
############################  
#File Name: dataset.py
#Author: linengier  
#Mail: linengier@126.com  
#Created Time: 2018-11-18 13:57:10
############################ 
from math import log
import operator
# 计算数据集合的熵
def calc_shannon_ent(dataSet):
    #calcuate all data num
    numEntries = len(dataSet)

    labelcounts = {}
    
    for featVec in dataSet:
        currentlabel =   featVec[-1]
        if currentlabel not in labelcounts.keys():
            labelcounts[currentlabel] = 0
        labelcounts[currentlabel] += 1

    shannoEnt = 0.0

    for key in labelcounts:
        prob =  float(labelcounts[key]) / numEntries
        shannoEnt -= prob*log(prob, 2)
    return shannoEnt



def createDataSet():
    dataSet = [[1,1,'yes'],
            [1,1,'yes'],
            [1,0,'no'],
            [0,1,'no'],
            [0,1,'no']]
    lables = ['no surfaceing', 'flippers']
    return dataSet, lables




# --------------------------------------------------------------------------
##
# @Synopsis  取具有相同特征的元素，并返回除了特征的其他元素 
#
# @Param dataSet  数据集
# @Param axisi    元素的类型
# @Param value    元素的值
#
# @Returns   
# append  添加整个元素
# extend  添加所有的元素
# ----------------------------------------------------------------------------
def spliteDataset(dataSet, axis, value):
    retdataset = []
    for featvect in dataSet:
        #特征上的值相等
        if featvect[axis] == value:
            reduceFeatVect = featvect[:axis]
            reduceFeatVect.extend(featvect[axis+1:])
            retdataset.append(reduceFeatVect)
    return retdataset
   

# --------------------------------------------------------------------------
##
# @Synopsis   选取信息集合的最优分类特征
#
# @Param dataset 数据集
#
# @Returns   该集合下最佳特征
# ----------------------------------------------------------------------------
def chose_best_Featrue_splite(dataset):
    #计算特征个数
    # 以信息集中的第一个元素，计算所有的特征
    numfeatures = len(dataset[0]) - 1

    #计算总体的信息熵
    baseEntropy = calc_shannon_ent(dataset)
    
    #定义最大信息增益
    bestinfoGain = 0.0
    beatFeature = -1

    # 遍历每一个特征
    #对特征下的每一个特征进行集合划分
    #求的子集合的概率和信息熵
    #计算信息增益
    for i in range (numfeatures):
        #创建分类标签列表
        #统计特征所有的值
        featList = [example[i] for example in dataset]
        #获得元素的集合
        uniqueVals = set(featList)
         
        newEntropy = 0.0
        
        #根据特征的特征值，计算信息增益和
        for val in uniqueVals:
            subdataset = spliteDataset(dataset, i, val)
            prob = len(subdataset)/ float(len(dataset))
            #概率*（该特征下，分类的信息增益）
            newEntropy += prob*calc_shannon_ent(subdataset)
        #信息熵 - 条件信息熵 = 信息增益
        #信息增益，表示特征划分信息聚合程度， 越大越好
        #一定为正值？
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestinfoGain):
            bestinfoGain = infoGain
            bestFeature = i
    return bestFeature


def  majorityCnt(classlist):
    classcount ={}
    #类别数量统计
    for vote in classlist:
        if vote not in classcount.keys():
            classcount[vote] = 0
        classcount[vote] += 1
    # 数量排序
    sorted_classcount = sorted(classcount.iteritems(),\
            key = operator.itemgetter(1), reverse=True)
    return sorted_classcount[0][0]

def creat_tree(dataset, labels):
    #得到所有的分类
    classlist = [example[-1] for example in dataset]


    # 判断是否结束
    ##判断数据集中元素类别相同
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    
    ##只有一个特征时，选择出现次数最多的类别
    if len(dataset[0]) == 1:
        return 1

    #选择最优的节点
    bestFeat = chose_best_Featrue_splite(dataset)
    bestFeatLabel = labels[bestFeat]
    
    #节点加入字典中
    mytree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    #根据最优节点的值划分子集

   # 根据最优特征的值，划分子集
    featValues = [example[bestFeat] for example in dataset]
    uniqueVals = set(featValues)

    for value in uniqueVals:
        sublables = labels[:]
        mytree[bestFeatLabel][value] = creat_tree(\
               spliteDataset(dataset, bestFeat, value), sublables)

    return mytree


if __name__ == "__main__":
    mydata, labels  = createDataSet()
    print mydata
    print calc_shannon_ent(mydata)
    '''
    mydata[0][-1] = 'maybe'
    print calc_shannon_ent(mydata)
    '''
    #按照特征0，值分别为1，0划分集合
    print spliteDataset(mydata, 0, 1)
    print spliteDataset(mydata, 0, 0)


    print "tree node: ", chose_best_Featrue_splite(mydata)
    


    print "tree", creat_tree(mydata, labels)
