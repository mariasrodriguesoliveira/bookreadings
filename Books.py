#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:29:49 2020

@author: maria
"""
import datetime
import requests
import xmltodict
import pandas as pd


resp = requests.get('https://www.goodreads.com/review/list?v=2', params=  {'key':'pycN2ACGte2YWrR9BPgvBw', 'v': 2, 'id': 117499894, 'per_page': 200}) #I've chosen this Goodreads API method to get my account readings information. Id is my account/user id and the max of books per page is 200. Response in xml
data_dict = xmltodict.parse(resp.content)['GoodreadsResponse'] #convert from xml to dictionary and below created all relevant columns for my final dashboard

data_dict['title'] = []
data_dict['author'] = []
data_dict['publisher'] = []
data_dict['publish_date'] = []
data_dict['average_rating'] = []
data_dict['description'] = []
data_dict['image'] = []
data_dict['country'] = []
data_dict['status'] = []

for i in range(0, len(data_dict['reviews']['review'])): #this goes through all books in my shelves (to read, read and currently reading) Later on this is distinguised by field "status"
    data_dict['title'].append(data_dict['reviews']['review'][i]['book']['title'])   
    data_dict['author'].append(data_dict['reviews']['review'][i]['book']['authors']['author']['name'])
    data_dict['publisher'].append(data_dict['reviews']['review'][i]['book']['publisher'])
    
    
    if type(data_dict['reviews']['review'][i]['book']['publication_day']) is not str: #this condition deals with unknown book publish dates
        publishdate = datetime.date(1900,1,1)     
    else:
        publishdate = datetime.date(int(data_dict['reviews']['review'][i]['book']['publication_year']), 
        int(data_dict['reviews']['review'][i]['book']['publication_month']),
        int(data_dict['reviews']['review'][i]['book']['publication_day']))   #concatenating the three fields as a single date

    data_dict['publish_date'].append(publishdate)
    data_dict['average_rating'].append(data_dict['reviews']['review'][i]['book']['average_rating'])
    
    if type(data_dict['reviews']['review'][i]['book']['description']) is not str:
        book_description = 'NA'     
    else:
        book_description = data_dict['reviews']['review'][i]['book']['description']
                                    
    data_dict['description'].append(book_description)
    data_dict['status'].append(data_dict['reviews']['review'][i]['shelves']['shelf']['@name']) #useful to separate shelves (to-read, read, currently reading)

del data_dict['image'] # Due to image quality, this column will be merged from Excel file below
del data_dict['country']
del data_dict['reviews'] #non relevant columns
del data_dict['Request']


BooksAPI = pd.DataFrame([data_dict]) #creats a table from dictionary data:dict
BooksAPI.info()

BooksAPI = BooksAPI.apply(pd.Series.explode).reset_index(drop=True) # explode rows

BooksExcel = pd.read_excel("Book readings with Power BI.xlsx") #reads excel with my personal notes, category, image url, my ratings etc, this gives me more flexibility than simply using Goodreads account

BookPowerBI = BooksAPI[["title", 
                         "author", 
                         "publisher", 
                         "publish_date", 
                         "average_rating", 
                         "description", 
                         "status" ]].merge(BooksExcel[["title",
                                                   "Reading Date",
                                                   "Category",
                                                   "Quotes",
                                                   "Notes/References",
                                                   "Rating",
                                                   "Image"]],
                                           on = "title",
                                           how = "left")
                                                                                                    

#script used as data source in Power BI (Dashboard tabs Readings and Parking Lot)









                               
    




