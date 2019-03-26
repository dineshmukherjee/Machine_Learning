# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 01:23:14 2019

@author: Admin
"""
import nltk
import random
import collections
from collections import Counter 

with open('alllines.txt','r') as data:
    cleanedText=data.read().replace('\n', '').replace('""',' ').replace("' ",'').replace('!','').replace('$','')
    cleanedText=cleanedText.replace("''",'').replace("(",'').replace(')','').replace('-','').replace('--','')
    cleanedText=cleanedText.replace("...",' ').replace(",",'').replace("'",'').replace('?','').replace('[','')
    cleanedText=cleanedText.replace(']','').replace(':','').replace("``",'')


cleanedText=cleanedText.lower()
newsList=cleanedText.split('.')

wordTokens=nltk.word_tokenize(cleanedText)

#Tracking the distribution of all the words
unigramDict={}
for word in wordTokens:
    if word in unigramDict:
        unigramDict[word] += 1
    else:
        unigramDict[word] = 1

#using inbuilt fuction to show th more frequent n items.
Counter = Counter(wordTokens) 
most_occur = Counter.most_common(10) 

print('\n Words Distribution with top 10 words:')
print(most_occur) 


#Words Correlation Logic.
bigrams = [b for l in newsList for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]

bigram_dict = collections.defaultdict(lambda: [0])
unigramTree={}

for team in bigrams:
    bigram_dict[team][0] +=1
    
    if(team[0] in unigramTree.keys()):
       if(team[0]!='' and team[1]!='' and team[0]!=None and team[1]!=None):        
           unigramTree[team[0]].extend([team[1]])
    else:
        if(team[0]!='' and team[1]!='' and team[0]!=None and team[1]!=None):
            unigramTree[team[0]]=[team[1]]

for key,val in bigram_dict.items():
        bigram_dict[key] = int(val[0])

correlation_dict={}
#for key,val in bigram_dict.items():
#    correlation_dict[key]=float(float(val)/((float(unigramDict[key[0]])+1) * (float( unigramDict[key[1]]) +1)))
#    
correlation_sorted = sorted(bigram_dict.items(), key=lambda kv: kv[1], reverse=True)

#top 5 correlated key value paris/words
print('\n Words correlation with top 10 words:')
i=0;
for key,val in correlation_sorted:
    if i==10:
        break
    print(key,val)
    i+=1


# Text Generation from the given text

activeItem= list(unigramTree.keys())[random.randint(0,len(unigramTree))]
newText=''

#genrate the new text with 30 words from copurs
print('\n Text Generation with 30 words:')
for i in range(1,30):

    try:     
        newText=newText+" "+activeItem
        index=random.randint(0,len(unigramTree[activeItem]))
        activeItem=unigramTree[activeItem][index]
        
        if(len(unigramTree[activeItem])==0):
            activeItem= list(unigramTree.keys())[random.randint(0,len(unigramTree))]
    except:
        activeItem= list(unigramTree.keys())[random.randint(0,len(unigramTree))]
        i=i-1

print(newText)    
    
    
# Sequence Generation

seqString = input('Enter the text:') 

seqList=seqString.split(' ')

lastWordBigrams=unigramTree[seqList[-1]]

prob=0
nextBestword=''
maxProb=0
for token in lastWordBigrams:
    for item in seqList:
    
        if (item,token) in bigram_dict:
            if(bigram_dict[(item,token)]==[0]):
                data=0
            else:
                data=int(bigram_dict[(item,token)])
        else:
            data=0
            
        if(prob==0):
            prob=data
        else:
            prob=prob*(data+.1)
    
    if(maxProb<prob) :   
        nextBestWord=token
        maxProb=prob
    prob=0

print(nextBestWord)

