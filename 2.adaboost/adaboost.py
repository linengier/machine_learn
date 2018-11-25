#/usr/bin/python  
#-*- coding:utf-8 -*-  
############################  
#File Name: adaboost.py
#Author: linengier  
#Mail: linengier@126.com  
#Created Time: 2018-11-25 22:46:41
############################ 
from numpy import *
def loadsimpdata():
    datamat = matrix([[1.,2.1],
            [2.,1.1],
            [1.3, 1.],
            [1., 1.],
            [2., 1.]])
    class_lables = [1.0, 1,0, -1.0, -1.0, 1.0]
    return datamat, class_lables
if __name__ == "__main__":
    data, labls = loadsimpdata()
    m, n = shape(data)
    print m, n
