import time
import jieba
import numpy as np
import re

def open_dict(Dict = "li", path = "H:\\anaconda\\envs\\py36\\sentiment\\"):
    path = path + "%s.txt" %Dict
    print(path)
    with open(path, "r", encoding = "UTF-8", errors = "ignore") as dictionary:
         dict = []
         for word in dictionary:
             word = word.strip("\n")
             dict.append(word)
             #json_str = simplejson.dumps(word, encoding="UTF-8", ensure_ascii=False)
             #print(json_str)
         #print(dict)
    return dict

ndict = open_dict(Dict = "negative-emotions")#负面情感词典
pdict = open_dict(Dict = "positive-emotions")#正面情感词典
degree_word = open_dict(Dict = "degree")#程度词词典

#为程度词设置权重
mostdict = degree_word[degree_word.index("most")+1 : degree_word.index('very')] #权重6
print(mostdict)
verydict = degree_word[degree_word.index('very')+1 : degree_word.index('more')] #权重5
print(verydict)
moredict = degree_word[degree_word.index('more')+1 : degree_word.index('ish')]#权重4
print(moredict)
ishdict = degree_word[degree_word.index('ish')+1 : degree_word.index('insufficiently')]#权重3
print(ishdict)
insuffidict = degree_word[degree_word.index('insufficiently')+1:degree_word.index('over')]#权重2
print(insuffidict)
overdict = degree_word[degree_word.index('over')+1 :degree_word.index('last')]#权重1
print(overdict)
seg_sentence = []

#分句
def cut_sent(infile, outfile):
    cutLineFlag = ["？", "！", "。","…",":"]
    sentenceList = []
    with open(infile, "r", encoding="UTF-8") as file:
        oneSentence = ""
        for line in file:
            words = line.strip()
            if len(oneSentence)!=0:
                sentenceList.append(oneSentence.strip() + "\n")
                oneSentence=""
            oneSentence = ""
            for word in words:
                if word not in cutLineFlag:
                    oneSentence = oneSentence + word
                else:
                    oneSentence = oneSentence + word
                    if oneSentence.__len__() > 4:
                        sentenceList.append(oneSentence.strip() + "\n")
                    oneSentence = ""
            #print(sentenceList)
            
    with open(outfile, "w", encoding="UTF-8") as resultFile:
        print(sentenceList.__len__())
        print("\n")
        resultFile.writelines(sentenceList)
    return sentenceList

#分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    f1 = "H:\\anaconda\\envs\\py36\\sentiment\\hit_stopwords.txt"#根据停用词词典进行分词
    with open(f1, 'r', encoding='utf-8') as fin:
         stopwords = fin
         outstr=""
         for word in sentence_seged:
             if word not in stopwords:
                if word!='\t':
                   outstr+=word
                   outstr+=" "
         #print(outstr)
         return outstr

#将分词结果写入文档
def w1():
    inputs=open(r"H:\\anaconda\\envs\\py36\\out.txt",'r',encoding='utf-8')#加载要处理的文件的路径
    outputs=open(r"H:\\anaconda\\envs\\py36\\out2.txt",'w',encoding='utf-8')#加载处理后的文件路径
    for line in inputs:
        line_seg = seg_sentence(line)#这里的返回值是字符串
        outputs.write(line_seg)
    outputs.close()
    inputs.close()
   
    
#判断得分
def sentiment_score_list(data):
    count2 = []
    count1 = []
    w1()
    #分句
    sentences = cut_sent(infile, outfile)
    #print(sentence)
    for sen in sentences:
       sen2 = sen.strip()
       seg_list = seg_sentence(sen2)#分词
       print(seg_list)
       i = 0
       j = 0
       p1 = 0
       n1 = 0
       for word in seg_list:
           if word in pdict:
               #print("p")
               p1 = p1+1
               for w in seg_list[j:i]:
                  if w in mostdict:
                      p1 = p1*6.0
                  elif w in verydict:
                      p1 = p1*5.0
                  elif w in moredict:
                      p1 = p1*4.0
                  elif w in ishdict:
                      p1 = p1*3.0
                  elif w in insuffidict:
                      p1 = p1*2.0
                  elif w in overdict:
                      p1 = p1*1.0
               j = i+1
           elif word in ndict:
               #print("n")
               n1 = n1+1
               for w in seg_list[j:i]:
                  if w in mostdict:
                      n1 = n1*6.0
                  elif w in verydict:
                      n1 = n1*5.0
                  elif w in moredict:
                      n1 = n1*4.0
                  elif w in ishdict:
                      n1 = n1*3.0
                  elif w in insuffidict:
                      n1 = n1*2.0
                  elif w in overdict:
                      n1 = n1*1.0           
               j = i+1
           i = i+1
           count1.append([p1,n1])#记录每个词得分
           #print(seg_list+'\n')
           #print(word)
       #print(p1, n1)
       #print(sen)
       count2.append(count1)
       count1 = []
    return count2

def sentiment_score(senti_score_list):
    score = []
    s = ""
    w = ""
    for score in senti_score_list:
        score_array =  np.array(score)
        #print(score_array)
        Pos = np.sum(score_array[:,0])#积极总分
        Neg = np.sum(score_array[:,1])#消极总分  
        #print(score)
        s+='\n'+str([Pos, Neg])
        score.append([Pos,Neg])
        res=Pos-Neg
        if res>0:
            w+='\n'+'好评'
            print ('该条评论是:好评')
        elif res<0:
            w+='\n'+'差评'
            print ('该条评论是：差评')
        else:
            w+='\n'+'中评'
            print ('该条评论得分是:中评')
    return w

data = open("H:\\anaconda\\envs\\py36\\date.txt","r",encoding = "utf-8", errors='ignore')
infile = "H:\\anaconda\\envs\\py36\\date.txt"
outfile = "H:\\anaconda\\envs\\py36\\out.txt"

#将函数返回结果存入s中
f = open('H:\\anaconda\\envs\\py36\\s.txt','w',errors='ignore')
f.write(sentiment_score(sentiment_score_list(data)))
f.close()



