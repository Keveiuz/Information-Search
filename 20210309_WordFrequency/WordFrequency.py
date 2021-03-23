# 1st. Data read in & Data Process & Frequency FILE Create #
import math
import re

## 1. Variables Declairation 声明变量
data = []
total = 0
lstFrequency = []
txtFrenquency = []
dicFrequency = {}

## 2. Data read-in & data Pre-process 文件读入与数据预处理
with open('/Users/jason/Documents/GitHub/Information_Search/20210309_WordFrequency/Test_Data/sw2078-ms98-a-trans.txt', 'r+') as dataFile:
    for line in dataFile.readlines():
        if line != None:
            data.append(line.strip('\n'))
dataProcessed = ' '.join(data).split(' ')

## 3.Build Dictionary & Calculate Frequency 建立字典与计算频率for word in dataProcessed :
for word in dataProcessed :
    dicFrequency[word] = dicFrequency.get(word, 0) + 1
    total += 1

## 4. Sortig Data 对结果排序
lstFrequency = list(dicFrequency.items())
print(lstFrequency)
lstFrequency.sort(key = lambda p: (-p[1], p[0]))

## 5. Texting Data 数据文本化（方便后续写入文档）for fr in lstFrequency:
for fr in lstFrequency:
    fr = list(fr)
    txtFrenquency.append(fr[0] + ':' + ' ' + str(fr[1]) + '\n')

Result = ''.join(txtFrenquency)

## 6. Create a WordFrequence File 创建字频文档fileOriginName = dataFile.name
fileName = dataFile.name

dot = re.compile('\.')                                  # Renaming 
fileName = re.sub(dot, '_Frequency.',fileName)          # Renaming 

ResultFile = open(fileName, 'w')
ResultFile.write(Result)

dataFile.close()
ResultFile.close()


#***************************************************************************


# 2nd. Data Data Visualization with Matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## 1. Variables Declairation 声明变量
topWords = []
totalOrigin = total

class topWord:
    def __init__(self, word, frequency):
        self.word = word
        self.frequency = frequency

## 2.Search Top-5 Words 统计出现次数最多的五个单词   
for i in range(0, 5):
    tmp = topWord(lstFrequency[i][0], lstFrequency[i][1])
    topWords.append(tmp)
    total -= lstFrequency[i][1]

print(topWords, total)

## 3. Ploting Figure 作图
plt.figure(figsize=(3, 2), dpi=300, facecolor='#f2f2f2')

plt.title('Words Appearance Proportion', fontdict={'fontweight': '600', 'fontsize': '10'})

Labels = [topWords[0].word, topWords[1].word, topWords[2].word, topWords[3].word, topWords[4].word, 'Others']
Values = [topWords[0].frequency, topWords[1].frequency, topWords[2].frequency, topWords[3].frequency, topWords[4].frequency, total]
Colors = ['#F25C5C', '#FFCA40', '#6B98F2', '#2E8C83', '#402CBF', '#c6cdd7']

patches, texts, autotexts = plt.pie(Values, labels = Labels, colors=Colors, autopct = '%.2f %%', pctdistance = 0.8, labeldistance = 1.2, startangle = 30, textprops={'size': '6'}, counterclock=False)
plt.setp(autotexts, size='3')

autotexts[3].set_color('white'),autotexts[4].set_color('white')

plt.legend(loc="upper right",fontsize=4,bbox_to_anchor=(-0.1,1),borderaxespad=0.3)


## 4.File Renaming & Figure Saving 文件重命名与图像储存
fileOriginName = dataFile.name

form = re.compile('(\.).*')                                 
PltName = re.sub(form, '_Proprotion.jpeg',fileOriginName)         
plt.savefig(PltName , dpi=300) 

plt.show()