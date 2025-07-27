# -*- coding: utf-8 -*-
"""
Created on Mon May  8 20:52:34 2023

@author: Liji
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd

#initializing the dataframe
df = pd.DataFrame(columns = ['datePublished','user', 'text_header',"verified", 'text_content','Aircraft','Type Of Traveller', 'Seat Type', 'Route', 'Date Flown', 'Seat Comfort', 'Cabin Staff Service', 'Food & Beverages','Inflight Entertainment', 'Ground Service','Wifi & Connectivity', 'Value For Money', 'Recommended'])
#k : to iterate the dataframe starting from zero ; P is to iterate through the paginations
#Initializing the page and dataframe
k=0
p=1
#Extracting the required details from different pages 
total_pages=18
while p<=total_pages:
#
    print(p)
    URL="https://www.airlinequality.com/airline-reviews/air-india/page/"+str(p)+"/?sortby=post_date%3ADesc&pagesize=100"
   # URL="https://www.airlinequality.com/airline-reviews/air-india-express/page/"+str(p)+"/?sortby=post_date%3ADesc&pagesize=100"
    #URL = "https://www.airlinequality.com/airline-reviews/air-india/?sortby=post_date%3ADesc&pagesize=100/page/"+str(p)+"/"
    print(URL)
    p=p+1
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results= soup.findAll("article",{"itemprop":"review"})
    print(len(results))
#    k=0
    datalist=[]
    for result in results:
        rows = []
        df.loc[k] = ["NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA"]
#        print(result)
        review_date= result.findAll("time",{"itemprop":"datePublished"})
        
    #    print(review_date[0].text)
        date = review_date[0].text.strip()
        df.loc[k ,'datePublished']=date
        reviewer_name= result.findAll("span",{"itemprop":"name"})
        user= reviewer_name[0].text.strip()
        df.loc[k ,'user']=user
       
#        rows.append('datePublished:'+date)
#        df = df.append('datePublished',date)
        review_title= result.findAll("h2",{"class":"text_header"})
    #    print(review_title[0].text)
        title = review_title[0].text.strip() 
#        rows.append('text_header:'+title)
        df.loc[k ,'text_header']=title
       
#        df = df.append('text_header',title)
#        k=k+1
      
        review_body= result.findAll("div",{"class":"text_content"})
    #         print(review_body[0])
        content = review_body[0].text.strip() 
        content_splt=content.split("|")
#        rows.append('text_content:'+content)
#        print(len(content_splt))
        if(len(content_splt)==2):
            df.loc[k ,'verified']=content_splt[0]       
            df.loc[k ,'text_content']=content_splt[1]
        else:
            df.loc[k ,'text_content']=content_splt[0] 
            
        review_data=result.findAll("table",{"class":"review-ratings"})
        for i, row in enumerate(review_data[0].find_all('tr')):
#             print(i,row)   
             el=row.find_all('td')
             row_title= el[0].text.strip()  
             x = el[1].find_all('span',{"class":"star fill"})
#                 print(x,"###########")
#                 x = el.find_all('td',{"class":"review-value"})
             if(x==None or x==[]):
#                 print(el.text.strip())
                 row_value=(el[1].text.strip())
             else:
#                 print(len(x), "################@@@@@@@@@@@@")
#                     star=x.find_all()      
                 row_value= str(len(x))
#             print(row_title+":"+row_value)    
             df.loc[k ,row_title]=row_value
     
#        datalist.append(rows) 
#        df.append({rows}, ignore_index=True)
       
        k=k+1
df.to_csv("AirIndia_Review_From_airquality.csv")     

  