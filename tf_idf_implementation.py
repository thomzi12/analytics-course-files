
# coding: utf-8

#Program that takes in data, and shingles each search term

import numpy as np
import pandas as pd

#load csv data 

df = pd.read_csv('./train_subset.csv', encoding="ISO-8859-1") #Note: don't forget the "." when determining the file location
#list(df)  #Check column names of pandas dataframe 

delete = pd.read_csv('./train_subset.csv', encoding="ISO-8859-1")
delete.head(n =5)

# Force lowercase and whitespace

#Stemming code ... need to install the package in the environment though 
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('english')

# May re-write as a function at some point 
for i in range(0, len(df['search_term'])):
    df['search_term'].ix[i] = df['search_term'].ix[i].lower()
    df['search_term'].ix[i] = df['search_term'].ix[i].replace(" ", "")
    df['search_term'].ix[i] = stemmer.stem(df['search_term'].ix[i]) 
    

df['search_term'].isnull().sum() #Check for missing values #0


# Create k = 5 shingles and put into dictionary with index 
sd = {} # Shingle Dictionary
k = 3 # Size of shingle 

for i in range(0, len(df['search_term'])):
    list1 = [] 
    for j in range(0, len(df['search_term'].ix[i])):
        s = df['search_term'].ix[i][j:j+k]
        if(len(s)<k and len(list1) >0):
            break
        list1.append(s) # = Add created list to dictionary at ith index 
        
    sd[df['id'].ix[i]]=list1
#Print the result 

# Need to find a way, a loop, that stores where the one's occur in the characteristic matrix 
# Could build enormous dictionary that has each shingle as a key, and corresponding indices as a value in a list 

cm = {}
for i in sd.keys():
    for j in range(0,len(sd[i])):
        temp = sd[i][j]
        if temp not in cm:
            cm[temp] = [i]
        else:
            cm[temp].append(i) 
    

len(cm) #719 -- Number of shingles 

# Create 100 permutations of the list, put into matrix form

# Create a list from 0 to 700 we'll permutate on 
lst = []
for i in range(0,len(cm)):
    lst.append(i)

from random import shuffle
import numpy 

hash_table = numpy.zeros((len(cm), 100)) #Create empty hash table we'll fill in later
# hash_table

# fill in empty hash table with permutations of 0 ... [number of singles-1]
for i in range(0, len(lst)):
    temp = lst
    shuffle(temp)
    for j in range(0,len(hash_table[i])):
        hash_table[i][j] = temp[j]
   

# Create Signature table, with initial values at the number of singles (i.e. one above a permutation element could ever be)

sig_table = numpy.zeros((100, len(df['search_term'])))
sig_table.fill(len(lst))
sig_table #100x100 = # of hashes x # of search terms matrix .shape gives dimensions of a numpy matrix


# In[20]:

# So, this is a bit complicated -- basically, need to map 'search_term' index to 0 to 100 so that I can create 
# signature matrix with a column for each matrix 

mapr = {}
val = 0
for i in sd.keys():
    mapr[i] = val
    val = val +1
# mapr
        
# Fill in values of signature matrix using simulated min-hash algorithm 

r = 0
for key, columns in cm.items(): #Grab shingle and search term indices it appears in 
    hval = hash_table[r,] # A numpy.ndarray of the appropriate row from the hash-table 
    for i in columns: #For each index grabbed, when multiple are associated with a shingle 
        for j in range(0, len(sig_table[:,mapr[i]])): #Run through each row of the mapr[i]th column
            if hval[j] < sig_table[j,mapr[i]]:
                sig_table[j,mapr[i]] = hval[j] #Replace current value with hash value if lower 
    r = r+1
#     print(r)
        
b = 20 # hardcode number of bands
r = 5 #hardcode number of rows 
final_table = numpy.zeros((b, len(df['search_term']))) # create ndarray to put hash results in 

# Fill in values for final_table
for i in range(0, b):
    temp = sig_table[r*(i):r*(i)+r] # Create sub-table with 5 rows 
    for j in range(0, temp.shape[1]): #Look at each column of the sub-table
        bucket = sum(temp[:,j])%100 
        final_table[i,j] = bucket 

# Now, find the similarities between each pairing of columns ... 
import itertools
perms = itertools.combinations(range(final_table.shape[1]), 2)# Gets the combinations of two  
sim_d = {} #Create dictionary to store similiarities 
for p in perms: 
    seta = frozenset(final_table[:,p[0]]) #Get columns into easier to-use data type 
    setb = frozenset(final_table[:,p[1]]) 
    match = len(frozenset.intersection(seta,setb))
    sim = match/b # our estimate of Jacqard similarity 
    sim_d[p] = sim 

# Let's look at the combinations where the estimated similarity is greater than t = .8
t = .8 
p1 = { key:value for key, value in sim_d.items() if value > t }
len(p1) #7 search term pairs were singled out 

p1

# Create a function to see if the excerpted pairs are actually similar
for col1, col2 in p1: 
    print("Here are the columns we're considering:", col1, ",", col2)
    for real, assigned in mapr.items():
        if assigned == col1:
            row1 = int(real)
    for real, assigned in mapr.items():
        if assigned == col2:
            row2 = int(real)
    print(list(df[df['id']==row1]['search_term']))
    print(list(df[df['id']==row2]['search_term']))
    

