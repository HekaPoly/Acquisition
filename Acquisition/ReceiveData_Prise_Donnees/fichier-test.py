import numpy as np


generalPlotList=[[1,2,3],[4,5,6],[7,8,9],[10,11,12]]

# x=[]
# taille=len(generalPlotList)
# print(taille)



x=[None]*(len(generalPlotList))
for i in range (0,len(generalPlotList)):
    x[i] = np.arange(0, len(generalPlotList[i]), 1)
print(x)

