
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import re 
import requests
import pandas as pd
pd.set_option('max_colwidth', 800)


# In[2]:


df=pd.read_excel('cik_list.xlsx')
sw=pd.read_csv('StopWords_Generic.txt',names='s')
sw.head()


# In[3]:


s=pd.read_csv('/home/vivek/Documents/Code/Blackcoffer/LoughranMcDonald_MasterDictionary_2016.csv')
dn=pd.DataFrame()
dp=pd.DataFrame()
dn['nword']=s['Word'].where(s['Negative']>0,0)

dn=dn.loc[(dn!=0).any(axis=1)]                                           #dropping zero values
dn = dn.reset_index(drop=True) 
dn.head()


# In[4]:


dp['pword']=s['Word'].where(s['Positive']>0,0)
dp=dp.loc[(dp!=0).any(axis=1)]
dp = dp.reset_index(drop=True)
dp.head()


# In[5]:


df['SECFNAME']='https://www.sec.gov/Archives/'+ df['SECFNAME']
df.head()


def pol(l):
    p=0
    n=0
    for i in l:
        for j in dn['nword']:
            if(i==j):
                n+=1
        for j in dp['pword']:
            if(i==j):
                p+=1
    return n,p


# In[7]:


asl="hello ABLE abandon"
pol(asl)


# # for stop words
# 

# In[8]:


def Stop(l):
    f=0
    l=list(l)
    for i in range(0,len(l),200):
        for j in sw['s']:
             if j  in l:
                    f=l.index(j)
                    del l[f]
    return len(l),l


# # for sentences

# In[9]:


def sen(s):
    s=str(s)
    a=0
    cleanr = re.compile('<.*?>')
    ct = re.sub(cleanr, '',s)
    for c in "\n=,)1234:;5678](\['-90*$%/":
        ct=ct.replace(c,' ')
        ct=ct.lower()
    for i in ct:
        if(i=='.'):
            a+=1
        
    return a
    


# # for uncertainty and constraining

# In[10]:


def uc(l):
    C=0
    U=0
    c=pd.read_excel('constraining_dictionary.xlsx')
    u=pd.read_excel('uncertainty_dictionary.xlsx')
    for i in c['Word']:
        if i in l:
            C+=1
    for j in u['Word']:
        if j in l:
            U+=1
    return U,C

# # for words

# In[12]:


def words(l):
    w=0
    i=0
    cleanr = re.compile('<.*?>')
    ct = re.sub(cleanr, '',l)
    for c in ".\n=,)1234@&#“:;5678](\['-90!?-^`*$%/":
        ct=ct.replace(c,' ')
        ct=ct.upper()
        l=ct.split()
    b=len(l)
    while i<b:
        if(len(l[i])<3 and l[i]!='A'):
            del l[i]
            i-=1
        b=len(l)
        i+=1
    return len(l),l



# # mda section

# In[24]:


k=[]
U=[]
C=[]
p=[]
n=[]
tw=[]
score=0
Sscore=0
stop=[]
ps=[]
ss=[]
fi=[]
asl=[]
pcw=[]
ns=[]
nw=[]
pp=[]
np=[]
cp=[]
up=[]
for j in df['SECFNAME'].head(25):
    Tw=0
    w=h=z=r=u=0
    r=requests.get(j)
    t=r.text
    soup=BeautifulSoup(t,'html.parser')
    s=str(soup)
    l=[]
    v=s.split('<page>')
    for i in v:
            if "MANAGEMENT\'S DISCUSSION AND\n " in i:
                    l.append(i)
            if "ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS" in i:
                l.append(i)
    if len(l)>1:  
        s=str(l[1:])
    else:
        s=str(l)
    h=sen(s)
    ns.append(h)
    if(n!=0):
        k.append(j)
    else:
        k.append('')
    w,d=words(s)
    tw.append(w)
    z,cww=Stop(d)
    stop.append(z)
    a,b=pol(d)
    if a==0:
        pp.append(0)
    else:
        pp.append((b/a))
    if b==0:
        np.append(0)
    else:
        np.append((a/b))
    p.append(b)
    n.append(a)
    nw.append(w)
    score=(b-a)/(b+a+0.000001)
    ps.append(score)
    Sscore=(b+a)/(w+0.000001)
    ss.append(Sscore)
    if h==0:
        u=0
    else:
        u=w/h
    if w==0:
        r=0
    else:
        r=z/w
    asl.append(u)
    pcw.append(r)
    fi.append(0.4*(u+r))
    uu,cc=uc(cww)
    if cc==0:
        up.append(0)
    else:
        up.append((uu/cc))
    if uu==0:
        cp.append(0)
    else:
        cp.append((cc/uu))
    U.append(uu)
    C.append(cc)
df['mda_positive_score']=pd.DataFrame(p)
df['mda_negative_score']=pd.DataFrame(n)
df['mda_polarity_score']=pd.DataFrame(ps)
df['mda_avg_sentence_length']=pd.DataFrame(asl)
df['mda_percentage_of_words']=pd.DataFrame(pcw)
df['mda_fog_index']=pd.DataFrame(fi)
df['mda_complex_word_count']=pd.DataFrame(stop)
df['mda_word_count']=pd.DataFrame(nw)
df['mda_uncertainity_score']=pd.DataFrame(U)
df['mda_constraining_score']=pd.DataFrame(C)
df['mda_positive_word_proportion']=pd.DataFrame(pp)
df['mda_negative_word_proportion']=pd.DataFrame(np)
df['mda_uncertainty_word_proportion']=pd.DataFrame(up)
df['mda_constraining_word_proportion']=pd.DataFrame(cp)
df['link']=pd.DataFrame(k)
df=df.drop('link',axis=1)

print df.iloc[20:25]
# # for polarity



