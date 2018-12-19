
# coding: utf-8

# importing required packages
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# loading "cik_list" file
df=pd.read_excel("cik_list.xlsx")

# making a dataframe of link
df['SECFNAME1']='https://www.sec.gov/Archives/'+ df['SECFNAME']


# fetching one file from url
url=df['SECFNAME1'][0]
text_fetch=requests.get(url)

# loading stop word
stop=pd.read_csv("StopWords_Generic.txt",names="w")


# loading constraining_dictionary
constrain=pd.read_excel('constraining_dictionary.xlsx')  

# load uncertainty_dictionary
uncertain=pd.read_excel('uncertainty_dictionary.xlsx')


# loading LoughranMcDonald_MasterDictionary_2016
dictionary=pd.read_csv("LoughranMcDonald_MasterDictionary_2016.csv")


# finding the negative word from LoughranMcDonald_MasterDictionary_2016
neg_df=pd.DataFrame()
negative=dictionary.loc[dictionary['Negative']>0]
neg_df["negative"]=negative["Word"]
neg_df=neg_df.reset_index(drop=True)

# finding the positive word from LoughranMcDonald_MasterDictionary_2016
pos_df=pd.DataFrame()
positive=dictionary.loc[dictionary['Positive']>0]
pos_df["positive"]=positive["Word"]
pos_df=pos_df.reset_index(drop=True)


# function for calculating "positive score", "negative score" and "polarity score"
def score(txt):
    pos=0
    neg=0
    for i in txt:
        for j in pos_df["positive"]:
            if(i==j):
                pos=pos+1
        for j in neg_df["negative"]:
            if(i==j):
                neg=neg+1
    pol_score=(pos-neg)/(pos+neg+0.000001)
    return pos, neg, pol_score


# function for calculating "number of word" and "tokenize the para"
def words(l):
    i=0
    phrase=re.findall(r'[a-zA-Z_]+',l)
    b=len(phrase)
    while i<b:
        if(len(phrase[i])<3):
            del phrase[i]
            i-=1
        b=len(phrase)
        i+=1
    return float(len(phrase)),phrase


# function for calculating the "number of sentence" in a para
def num_sentence(txt):
    txt=str(txt)
    number= txt.count(".")
    return float(number)


# function for calculating "stop word" and "lenght of stop word"
def stop_word(txt):
    txt=list(txt)
    x=0
    for i in range(0,len(txt),200):
        for j in stop["w"]:
             if j  in txt:
                    x=txt.index(j)
                    del txt[x]
    return float(len(txt)),txt


# function for calculating “uncertainty score” and “constraining score”
def const_uncert(txt):
    constraining=0
    uncertainty=0
    for i in constrain["Word"]:
        if i in txt:
            constraining=constraining+1
    for j in uncertain["Word"]:
        if j in txt:
            uncertainty=uncertainty+1
    return constraining, uncertainty

# calculating all the variables for “Management's Discussion and Analysis”
positive_score=[]
negative_score=[]
polarity_score=[]
avg_sen_len=[]
fog_index=[]
word_count=[]
complex_word_count=[]
uncertainity_score=[]
constraining_score=[]
per_complex_word=[]
positive_word_proportion=[]
negative_word_proportion=[]
uncertainty_word_proportion=[]
constraining_word_proportion=[]
for i in df['SECFNAME1'].head(1):
    data=requests.get(i)
    data_text=data.text
    parse=BeautifulSoup(data_text,'html.parser')
    parse_string=str(parse)
    pages=parse_string.split('<page>')
    para=[]
    for i in pages:
            if "MANAGEMENT\'S DISCUSSION AND\n " or "ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS" in i:
                para.append(i)
    if len(para)>1:  
        str_para=str(para[1:])
    else:
        str_para=str(para)
    total_word,words=num_word(str_para)
    sentence_count=num_sentence(str_para)
    stop_word_count,stop_words=stop_word(words)
    const_count,uncert_count=const_uncert(words)
    positive,negative,polarity= score(words)
    positive_score.append(positive)
    negative_score.append(negative)
    polarity_score.append(polarity)
    if sentence_count==0:
        avg_sen=0
    else:
        avg_sen=(total_word/sentence_count)
    avg_sen_len.append(avg_sen)
    if total_word==0:
            per_complex=0
    else:
        per_complex=stop_word_count/total_word
    per_complex_word.append(per_complex)
    fog_index.append(0.4*(avg_sen+per_complex))
    complex_word_count.append(stop_word_count)
    word_count.append(total_word)
    uncertainity_score.append(uncert_count)
    constraining_score.append(const_count)
    if total_word==0:
        neg_word_prop=0
    else:
        neg_word_prop=negative/total_word
    negative_word_proportion.append(neg_word_prop)
    if total_word==0:
        pos_word_prop=0
    else:
        pos_word_prop=positive/total_word
    positive_word_proportion.append(pos_word_prop)
    if total_word==0:
        uncertainty_prop=0
    else:
        uncertainty_prop=uncert_count/total_word
    uncertainty_word_proportion.append(uncertainty_prop)
    if total_word==0:
        constrainty_prop=0
    else:
        constrainty_prop=const_count/total_word
    constraining_word_proportion.append(constrainty_prop)


# Generating the required datafrae
df['mda_positive_score']=pd.DataFrame(positive_score)
df['mda_negative_score']=pd.DataFrame(negative_score)
df['mda_polarity_score']=pd.DataFrame(polarity_score)
df['mda_avg_sentence_length']=pd.DataFrame(avg_sen_len)
df['mda_percentage_of_words']=pd.DataFrame(per_complex_word)
df['mda_fog_index']=pd.DataFrame(fog_index)
df['mda_complex_word_count']=pd.DataFrame(complex_word_count)
df['mda_word_count']=pd.DataFrame(word_count)
df['mda_uncertainity_score']=pd.DataFrame(uncertainity_score)
df['mda_constraining_score']=pd.DataFrame(constraining_score)
df['mda_positive_word_proportion']=pd.DataFrame(positive_word_proportion)
df['mda_negative_word_proportion']=pd.DataFrame(negative_word_proportion)
df['mda_uncertainty_word_proportion']=pd.DataFrame(uncertainty_word_proportion)
df['mda_constraining_word_proportion']=pd.DataFrame(constraining_word_proportion)



# calculating all the variables for “Quantitative and Qualitative Disclosures about Market Risk”
positive_score=[]
negative_score=[]
polarity_score=[]
avg_sen_len=[]
fog_index=[]
word_count=[]
complex_word_count=[]
uncertainity_score=[]
constraining_score=[]
per_complex_word=[]
positive_word_proportion=[]
negative_word_proportion=[]
uncertainty_word_proportion=[]
constraining_word_proportion=[]
for i in df['SECFNAME1']:
    data=requests.get(i)
    data_text=data.text
    parse=BeautifulSoup(data_text,'html.parser')
    parse_string=str(parse)
    pages=parse_string.split('<page>')
    para=[]
    for i in pages:
            if "Item 3.  Quantitative and Qualitative Disclosures About Market Risk" in i:
                para.append(i)
    para=str(para)
    para=para.split('Item 3')
    para=para[2:]
    str_para=str(para)
    total_word,words=num_word(str_para)
    sentence_count=num_sentence(str_para)
    stop_word_count,stop_words=stop_word(words)
    const_count,uncert_count=const_uncert(words)
    positive,negative,polarity= score(words)
    positive_score.append(positive)
    negative_score.append(negative)
    polarity_score.append(polarity)
    if sentence_count==0:
        avg_sen=0
    else:
        avg_sen=(total_word/sentence_count)
    avg_sen_len.append(avg_sen)
    if total_word==0:
            per_complex=0
    else:
        per_complex=stop_word_count/total_word
    per_complex_word.append(per_complex)
    fog_index.append(0.4*(avg_sen+per_complex))
    complex_word_count.append(stop_word_count)
    word_count.append(total_word)
    uncertainity_score.append(uncert_count)
    constraining_score.append(const_count)
    if total_word==0:
        neg_word_prop=0
    else:
        neg_word_prop=negative/total_word
    negative_word_proportion.append(neg_word_prop)
    if total_word==0:
        pos_word_prop=0
    else:
        pos_word_prop=positive/total_word
    positive_word_proportion.append(pos_word_prop)
    if total_word==0:
        uncertainty_prop=0
    else:
        uncertainty_prop=uncert_count/total_word
    uncertainty_word_proportion.append(uncertainty_prop)
    if total_word==0:
        constrainty_prop=0
    else:
        constrainty_prop=const_count/total_word
    constraining_word_proportion.append(constrainty_prop)


# Generating the required datafrae
df['qqdmr_positive_score']=pd.DataFrame(positive_score)
df['qqdmr_negative_score']=pd.DataFrame(negative_score)
df['qqdmr_polarity_score']=pd.DataFrame(polarity_score)
df['qqdmr_avg_sentence_length']=pd.DataFrame(avg_sen_len)
df['qqdmr_percentage_of_words']=pd.DataFrame(per_complex_word)
df['qqdmr_fog_index']=pd.DataFrame(fog_index)
df['qqdmr_complex_word_count']=pd.DataFrame(complex_word_count)
df['qqdmr_word_count']=pd.DataFrame(word_count)
df['qqdmr_uncertainity_score']=pd.DataFrame(uncertainity_score)
df['qqdmr_constraining_score']=pd.DataFrame(constraining_score)
df['qqdmr_positive_word_proportion']=pd.DataFrame(positive_word_proportion)
df['qqdmr_negative_word_proportion']=pd.DataFrame(negative_word_proportion)
df['qqdmr_uncertainty_word_proportion']=pd.DataFrame(uncertainty_word_proportion)
df['qqdmr_constraining_word_proportion']=pd.DataFrame(constraining_word_proportion)


# calculating all the variables for “Quantitative and Qualitative Disclosures about Market Risk”
positive_score=[]
negative_score=[]
polarity_score=[]
avg_sen_len=[]
fog_index=[]
word_count=[]
complex_word_count=[]
uncertainity_score=[]
constraining_score=[]
per_complex_word=[]
positive_word_proportion=[]
negative_word_proportion=[]
uncertainty_word_proportion=[]
constraining_word_proportion=[]
for i in df['SECFNAME1']:
    data=requests.get(i)
    data_text=data.text
    parse=BeautifulSoup(data_text,'html.parser')
    parse_string=str(parse)
    pages=parse_string.split('<page>')
    para=[]
    for i in pages:
            if "Item 3.  Quantitative and Qualitative Disclosures About Market Risk" in i:
                para.append(i)
    para=str(para)
    para=para.split('Item 3')
    para=para[2:]
    str_para=str(para)
    total_word,words=num_word(str_para)
    sentence_count=num_sentence(str_para)
    stop_word_count,stop_words=stop_word(words)
    const_count,uncert_count=const_uncert(words)
    positive,negative,polarity= score(words)
    positive_score.append(positive)
    negative_score.append(negative)
    polarity_score.append(polarity)
    if sentence_count==0:
        avg_sen=0
    else:
        avg_sen=(total_word/sentence_count)
    avg_sen_len.append(avg_sen)
    if total_word==0:
            per_complex=0
    else:
        per_complex=stop_word_count/total_word
    per_complex_word.append(per_complex)
    fog_index.append(0.4*(avg_sen+per_complex))
    complex_word_count.append(stop_word_count)
    word_count.append(total_word)
    uncertainity_score.append(uncert_count)
    constraining_score.append(const_count)
    if total_word==0:
        neg_word_prop=0
    else:
        neg_word_prop=negative/total_word
    negative_word_proportion.append(neg_word_prop)
    if total_word==0:
        pos_word_prop=0
    else:
        pos_word_prop=positive/total_word
    positive_word_proportion.append(pos_word_prop)
    if total_word==0:
        uncertainty_prop=0
    else:
        uncertainty_prop=uncert_count/total_word
    uncertainty_word_proportion.append(uncertainty_prop)
    if total_word==0:
        constrainty_prop=0
    else:
        constrainty_prop=const_count/total_word
    constraining_word_proportion.append(constrainty_prop)


# calculating all the variables for “Risk Factors”
positive_score=[]
negative_score=[]
polarity_score=[]
avg_sen_len=[]
fog_index=[]
word_count=[]
complex_word_count=[]
uncertainity_score=[]
constraining_score=[]
per_complex_word=[]
positive_word_proportion=[]
negative_word_proportion=[]
uncertainty_word_proportion=[]
constraining_word_proportion=[]
for i in df['SECFNAME1']:
    data=requests.get(i)
    data_text=data.text
    parse=BeautifulSoup(data_text,'html.parser')
    parse_string=str(parse)
    pages=parse_string.split('<div style="DISPLAY: block;')
    para=[]
    for i in pages:
            if "Risk Factors" in i:
                para.append(i)
    str_para=str(para)
    total_word,words=num_word(str_para)
    sentence_count=num_sentence(str_para)
    stop_word_count,stop_words=stop_word(words)
    const_count,uncert_count=const_uncert(words)
    positive,negative,polarity= score(words)
    positive_score.append(positive)
    negative_score.append(negative)
    polarity_score.append(polarity)
    if sentence_count==0:
        avg_sen=0
    else:
        avg_sen=(total_word/sentence_count)
    avg_sen_len.append(avg_sen)
    if total_word==0:
            per_complex=0
    else:
        per_complex=stop_word_count/total_word
    per_complex_word.append(per_complex)
    fog_index.append(0.4*(avg_sen+per_complex))
    complex_word_count.append(stop_word_count)
    word_count.append(total_word)
    uncertainity_score.append(uncert_count)
    constraining_score.append(const_count)
    if total_word==0:
        neg_word_prop=0
    else:
        neg_word_prop=negative/total_word
    negative_word_proportion.append(neg_word_prop)
    if total_word==0:
        pos_word_prop=0
    else:
        pos_word_prop=positive/total_word
    positive_word_proportion.append(pos_word_prop)
    if total_word==0:
        uncertainty_prop=0
    else:
        uncertainty_prop=uncert_count/total_word
    uncertainty_word_proportion.append(uncertainty_prop)
    if total_word==0:
        constrainty_prop=0
    else:
        constrainty_prop=const_count/total_word
    constraining_word_proportion.append(constrainty_prop)


# Generating the required datafrae
df['qqdmr_positive_score']=pd.DataFrame(positive_score)
df['qqdmr_negative_score']=pd.DataFrame(negative_score)
df['qqdmr_polarity_score']=pd.DataFrame(polarity_score)
df['qqdmr_avg_sentence_length']=pd.DataFrame(avg_sen_len)
df['qqdmr_percentage_of_words']=pd.DataFrame(per_complex_word)
df['qqdmr_fog_index']=pd.DataFrame(fog_index)
df['qqdmr_complex_word_count']=pd.DataFrame(complex_word_count)
df['qqdmr_word_count']=pd.DataFrame(word_count)
df['qqdmr_uncertainity_score']=pd.DataFrame(uncertainity_score)
df['qqdmr_constraining_score']=pd.DataFrame(constraining_score)
df['qqdmr_positive_word_proportion']=pd.DataFrame(positive_word_proportion)
df['qqdmr_negative_word_proportion']=pd.DataFrame(negative_word_proportion)
df['qqdmr_uncertainty_word_proportion']=pd.DataFrame(uncertainty_word_proportion)
df['qqdmr_constraining_word_proportion']=pd.DataFrame(constraining_word_proportion)
df.head()


# In[ ]:


# # Generating the solution file
df["SECFNAME"]=df["SECFNAME1"]
df.drop("SECFNAME1",axis=1)
df.to_csv('final.csv', encoding='utf-8', index=False)

