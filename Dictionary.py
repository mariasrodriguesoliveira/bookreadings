#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 21:36:50 2020

@author: maria
"""

import requests
import pandas as pd

dictionarypbi = pd.DataFrame() #TInitializing final table

dictionarywords = pd.read_excel("Book readings with Power BI.xlsx", sheet_name= "Dictionary") #This excel contains words for which I'm searching a definition. Returns a DataFrame
mylist = dictionarywords.values.tolist()
mylist = [''.join(ele) for ele in mylist] #converting DataFrame to List - easier to be used below

for i in range(0, len(mylist)):  
   
        resp = requests.get('https://www.dictionaryapi.com/api/v3/references/collegiate/json/' + mylist[i] + '?' + 'key=047ea979-2678-438b-aa9d-7de4ce3fe5e6') #Using Merriam-Webster's key for Collegiate® Dictionary with Audio  
        respostajson= resp.json() #Returns a list with one dictionary or a list of strings in case the word definition is not available in Merriam-Webster's 
        
        if type(respostajson[0]) is dict: #using this condition to avoid error from empty result (comment above)
                    
            try:                          #using try in this case due to definition structure differences for different words
                        
                wordinfo = respostajson[0]['def'][0]   #Initizalized wordinfo this way to avoid multiple index column errors. Note that this returns a dictionary thus being possible to add below columns: seacrhword and definition
 
                wordinfo['searchword'] = []
                wordinfo['definition'] = []

                wordinfo['searchword'].append(respostajson[0]['hwi']['hw'])
                wordinfo['definition'].append(wordinfo['sseq'][0][0][1][0][1]['dt'][0][1])
              
            except:
                wordinfo['searchword'].append(respostajson[0]['hwi']['hw'])
                wordinfo['definition'].append(wordinfo['sseq'][0][0][1]['dt'][0][1])  #definition structure alternative (there may be others)
      
            del wordinfo['sseq']
                
        else:
            print("NA") # for empty resutls/words not found
        
        pdauthorinfo = pd.DataFrame([wordinfo]) #comverting from dictionary to DataFrame
        tableauthor = pdauthorinfo.apply(pd.Series.explode).reset_index(drop=True)  #explode rows
        dictionarypbi = dictionarypbi.append(tableauthor) #appending i results for final table to be imported to Power BI 
        
        dictionarypbi = dictionarypbi.drop_duplicates() #This is the final table to be imported to power BI. Ideally with two columns: word and definition

del dictionarypbi['sls'] #Not able to delete all columns and some transformation will be done in Power BI Query editor

dictionarypbi.to_csv('dictionaryapi.csv')
