import math
import re

data = []

##******************__1.文件读入__**************************
with open('/Users/jason/Documents/GitHub/Information_Search/20210316_ChineseSegmentation/Test_Data/data_partial_utf8.txt', 'r+') as dataFile:
    for line in dataFile.readlines():
        if line != None:
            data.append(line.strip('\n'))


##******************__2.提取汉字和重要分隔符__*****************
dataString = ''.join(data)

charactor = re.compile('[\u4e00-\u9fa5\，\。\,\?\!\、\;]')
dataChineseOnly = charactor.findall(dataString)


##******************__3.检索字典词语最大长度__*****************
Dictionary = {}
MAXLENGTH = 0
with open('/Users/jason/Documents/GitHub/Information_Search/20210316_ChineseSegmentation/Test_Data/dict_utf8.txt', 'r+') as dictFile:
    for line in dictFile.readlines():   #按行读入
        if line != None:
                                        #构造词库字典
            Dictionary[line.strip('\n')] = Dictionary.get((line.strip('\n')), 1)                          
                                        
            if len(line) > MAXLENGTH:   #找到最大长度，并记为最大匹配长度
                MAXLENGTH = len(line)

##*****************__4.正向最大匹配__*****************************
#通过重要分隔符，把文段分割成短句，通过移动指针，在短句内实现最大匹配。（重要分隔符天然通过语义将文段分割，是提高分词准确率的基础）
breakingPoint = -1                      #指向重要分隔符的位置
paragraphLength = len(dataChineseOnly)  
headPointer = 0                         #指向片段始端
tailPointer = 0                         #指向片段末端
Pointer = 0                             #寻找重要分隔符的位置

forwordNotFound = {}                      #未匹配单字（未在字典中查询到）
forwordNotFoundTotal = 0                  #未匹配单字计数器
forwordFoundTotal = 0                     
forwordParaLength = 0
segmentationBuffer_0 = []                 #存放分割完成的字符串

#最大正向匹配算法与实现原理：
# （0）从文章开头寻找重要分隔符，分割短句     
# （1）在当前短句内，取最大长度，并将所取词放入字典匹配
# （2）若匹配成功，则导出该词；若失败，则缩短长度
# （3）若词长为1，则该词不再字典中
# （4）跳转到下一词继续匹配，直到匹配完整个短句
# （5）匹配完成后，寻找下一个重要分隔符，对下一个短句进行匹配，直到文章结束     

#（0）找到间断点（重要分隔符）
while breakingPoint < paragraphLength - 1:          #间断点在范围内

    headPointer = breakingPoint + 1                 #头指针指向上一个重要分隔符的下一位       

    while Pointer < paragraphLength:                #在文章长度范围内，寻找下一个重要分隔符
        if (dataChineseOnly[Pointer] == '，') or (dataChineseOnly[Pointer] == '。') or (dataChineseOnly[Pointer] == ',') or (dataChineseOnly[Pointer] == '?') or (dataChineseOnly[Pointer] == '!') or (dataChineseOnly[Pointer] == ';') or (dataChineseOnly[Pointer] == '、'):
            breakingPoint = Pointer             
            Pointer += 1
            break 
        Pointer += 1

    #***********匹配单个词语（每次）*************
    while headPointer < breakingPoint:              #保证该词在当前短句内

        tailPointer = headPointer + MAXLENGTH - 1   #尾指针初始化指向最大长度处
        if tailPointer >= breakingPoint:            #越界判断
            tailPointer = breakingPoint - 1

        flag = False                                #标记该词是否可在字典中检索到
        while tailPointer >= headPointer :          
            segmentation = ''.join(dataChineseOnly[headPointer:tailPointer+1])
            if segmentation in Dictionary :         #检索
                segmentationBuffer_0.append(segmentation) 
                forwordFoundTotal += 1 
                forwordParaLength += len(segmentation)
                flag = True                         #检索成功
                break

            else :
                tailPointer -= 1                    #查找失败，减短长度继续查找

        if flag == False :                          #检索失败
            segmentation = dataChineseOnly[headPointer]
            segmentationBuffer_0.append(segmentation)

            forwordNotFound[segmentation] = forwordNotFound.get(segmentation)     #将单字加入未知列表
            forwordNotFoundTotal += 1                      #检索失败计数器

            tailPointer += 1                        #此时的尾指针在头指针之前一位，通过加一实现复位 

        headPointer = tailPointer + 1               #头指针指向下一个词的开始位置
        #如此循环，直到该短句内所有词语都匹配完成

    segmentationBuffer_0.append(dataChineseOnly[breakingPoint])  

##**********************************************
fileName = dataFile.name

dot = re.compile('\.')
fileName = re.sub(dot, '_Forword.', fileName)

result = '/'.join(segmentationBuffer_0)

resultFile = open(fileName, 'w')
resultFile.write(result)



##*****************__5.反向最大匹配__*****************************
#通过重要分隔符，把文段分割成短句，通过移动指针，在短句内实现最大匹配。（重要分隔符天然通过语义将文段分割，是提高分词准确率的基础）
breakingPoint = paragraphLength - 1     #指向重要分隔符的位置
paragraphLength = len(dataChineseOnly)  
headPointer = breakingPoint - 1                         #指向片段始端
tailPointer = breakingPoint - 1                         #指向片段末端
Pointer = paragraphLength - 2                             #寻找重要分隔符的位置

reverseNotFound = {}                    #未匹配单字（未在字典中查询到）
reverseNotFoundTotal = 0                #未匹配单字计数器
reverseFoundTotal = 0
reversePrarLength = 0
segmentationBuffer_1 = []                 #存放分割完成的字符串

#反向最大匹配算法与实现原理：
# （0）从文章结尾寻找重要分隔符，分割短句     
# （1）在当前短句内，取最大长度，并将所取词放入字典匹配
# （2）若匹配成功，则导出该词；若失败，则缩短长度
# （3）若词长为1，则该词不再字典中
# （4）跳转到上一词继续匹配，直到匹配完整个短句
# （5）匹配完成后，寻找上一个重要分隔符，对上一个短句进行匹配，直到文章结束     

#（0）找到间断点（重要分隔符）
while breakingPoint > 0 :          #间断点在范围内

    tailPointer = breakingPoint - 1                 #头指针指向上一个重要分隔符的上一位       

    while Pointer > 0:                #在文章长度范围内，寻找上一个重要分隔符
        if (dataChineseOnly[Pointer] == '，') or (dataChineseOnly[Pointer] == '。') or (dataChineseOnly[Pointer] == ',') or (dataChineseOnly[Pointer] == '?') or (dataChineseOnly[Pointer] == '!') or (dataChineseOnly[Pointer] == ';') or (dataChineseOnly[Pointer] == '、'):
            breakingPoint = Pointer   
            segmentationBuffer_1.append(dataChineseOnly[breakingPoint])           
            Pointer -= 1
            break 
        Pointer -= 1

    if Pointer == 0:
        breakingPoint = -1

    #***********匹配单个词语（每次）*************
    while tailPointer > breakingPoint:              #保证该词在当前短句内

        headPointer = tailPointer - MAXLENGTH + 1   #尾指针初始化指向最大长度处
        if headPointer <= breakingPoint:            #越界判断
            headPointer = breakingPoint + 1

        flag = False                                #标记该词是否可在字典中检索到
        while headPointer <= tailPointer :          
            segmentation = ''.join(dataChineseOnly[headPointer:tailPointer+1])
            if segmentation in Dictionary :         #检索
                segmentationBuffer_1.append(segmentation)  
                reverseFoundTotal += 1
                reversePrarLength += len(segmentation)
                flag = True                         #检索成功
                break

            else :
                headPointer += 1                    #查找失败，减短长度继续查找

        if flag == False :                          #检索失败
            segmentation = dataChineseOnly[tailPointer]
            segmentationBuffer_1.append(segmentation)

            reverseNotFound[segmentation] = reverseNotFound.get(segmentation)     #将单字加入未知列表
            reverseNotFoundTotal += 1                      #检索失败计数器

            headPointer -= 1                        #此时的尾指针在头指针之前一位，通过加一实现复位 

        tailPointer = headPointer - 1               #头指针指向下一个词的开始位置
        #如此循环，直到该短句内所有词语都匹配完成 


##**********************************************
fileName = dataFile.name

dot = re.compile('\.')
fileName = re.sub(dot, '_Reverse.', fileName)

segmentationBuffer_1 = segmentationBuffer_1[::-1]
result = '/'.join(segmentationBuffer_1)

resultFile = open(fileName, 'w')
resultFile.write(result)


print('forwordNotFoundTotal: {:,}\nreverseNotFoundTotal: {:,}\nforwordFoundTotal: {:,}\nreverseFoundTotal: {:,}\nforwordAverageLength: {:.6f}\nreverseAverageLength: {:.6f}\n'.format(forwordNotFoundTotal,reverseNotFoundTotal,forwordFoundTotal,reverseFoundTotal,forwordParaLength/forwordFoundTotal,reversePrarLength/reverseFoundTotal))