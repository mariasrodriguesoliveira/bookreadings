#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 18:11:58 2020

@author: maria
"""

import datetime
import requests
import xmltodict
import pandas as pd


resp = requests.get('https://www.goodreads.com/review/list?v=2', params=  {'key':'pycN2ACGte2YWrR9BPgvBw', 'v': 2, 'id': 117499894, 'per_page': 200}) #same Request method used in Books previous script
authorid = xmltodict.parse(resp.content)['GoodreadsResponse']

authorid['id'] = [] 

for i in range(0, len(authorid['reviews']['review'])):  
    authorid['id'].append(authorid['reviews']['review'][i]['book']['authors']['author']['id']) #This time only retrieving authors id to be used as a parameter in below request
    

del authorid['reviews']
del authorid['Request']

authorlist = list(set(authorid['id'])) #listing unique author ids


#------------------------------------------------------------------------------

authorsAPI = pd.DataFrame()

for i in range(0, len(authorlist)):
    resp1 = requests.get('https://www.goodreads.com/author/show.xml', params=  {'key':'pycN2ACGte2YWrR9BPgvBw', 'id': authorlist[i], 'page': 200}) #Used this Goodreads API method to retrieve authors data
    authorinfo = xmltodict.parse(resp1.content)['GoodreadsResponse']

    authorinfo['name'] = []
    authorinfo['books'] = []
    authorinfo['publish_date'] = []
    authorinfo['avg_rating'] = []


    for j in range(0, len(authorinfo['author']['books']['book'])):
        try:
            authorinfo['books'].append(authorinfo['author']['books']['book'][j]['title']) 
            authorinfo['name'].append(authorinfo['author']['name'])
            authorinfo['avg_rating'].append(authorinfo['author']['books']['book'][j]['average_rating']) 


            if type(authorinfo['author']['books']['book'][j]['publication_day']) is not str:
                publishdate = datetime.date(1900,1,1)     
            else:
                publishdate = datetime.date(int(authorinfo['author']['books']['book'][j]['publication_year']), 
                                        int(authorinfo['author']['books']['book'][j]['publication_month']),
                                        int(authorinfo['author']['books']['book'][j]['publication_day']))   

            authorinfo['publish_date'].append(publishdate)
        except:
            print("Error due to authors with single book")
            
    del authorinfo['Request']
    del authorinfo['author'] #non relevant columns
 
    pdauthorinfo = pd.DataFrame([authorinfo])
    tableauthor = pdauthorinfo.apply(pd.Series.explode).reset_index(drop=True)  
    authorsAPI = authorsAPI.append(tableauthor)


                                                          
authorsAPI.to_csv('authorsapi.csv') #It's more efficient and much faster to use this csv as data source in PowerBI than the full script, also limiting number of requests

#merging with authors image url in PBI. main goal of this script is to try timeline storyteller visual in PBI - looks interesting!

    