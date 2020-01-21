# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 09:54:44 2020

@author: infomax
"""

import sys
import mechanicalsoup
from bs4 import BeautifulSoup

movie_list = []

for i in range(1,6000,100) :
#for i in range(1,10,100) :

    address = "https://www.the-numbers.com/movie/budgets/all" 

    if i > 1 :
        address += "/" + str(i)
    
    data = mechanicalsoup.Browser().get(address)

    lists = data.soup.findAll('tr')
    #lists = data.soup.findAll('td' , attrs={ 'class' : "data" } )

    for list in lists :
        #print(list)
        
        cdata = list.find('td', attrs={ 'class' : "data" } )
        
        if cdata is not None :
            tmp = {}
            tds = list.findAll('td')
            aa = tds[1].find('a')
            #print (aa["href"])            
            ba = tds[2].find('a')
            #print (ba.text)
            tmp["movies"] = ba.text
            tmp["release_date"] = aa["href"][-10:]
            tmp["budget"] = tds[3].text
            tmp["dom_gross"] = tds[4].text
            tmp["world_gross"] = tds[5].text
            tmp["href"] = ba["href"]
            movie_list.append(tmp)
                
        
# %%
from tqdm import tqdm
            
for movie in tqdm(movie_list) :
    
    if "mpaa-rating" not in movie.keys() and "2020/" not in movie["release_date"] and "20" == movie["release_date"][:2] :        
        
        address = "https://www.the-numbers.com" + movie["href"]
        
        data = mechanicalsoup.Browser().get(address)
        
        lists = data.soup.findAll('a')
        
        for list in lists : 
            try :
                if "/market/mpaa-rating" in list["href"] :
                    #print ( movie["movies"], list["href"],  list.text )
                    movie["mpaa-rating"] = list.text
                    break
            except KeyError :
                print ( list )

        else : 
            movie["mpaa-rating"] = "NotRated"
# %%
    
for movie in movie_list :
    #if len(movie.keys()) == 6 and "2020/" not in movie["release_date"] and "19" == movie["release_date"][:2] :
    #    print (movie)
    print (movie["movies"].encode("ascii","ignore").decode("ascii"))
                
# %%                
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', passwd='1111', db='mysql' , charset='utf8')
cur = conn.cursor()
            

for movie in tqdm(movie_list) :        
    
    try :
        mpaa_rating = movie["mpaa-rating"]
    except KeyError :
        mpaa_rating = ""            
        
    if movie["release_date"][:2] != "20" and movie["release_date"][:2] != "19" :
        release_date = "2020/12/31"
    else :
        release_date = movie["release_date"]
        
    #try :    
    cur.execute( u'insert into tbMoviesBudgetPL (title, release_date, budget, dom_gross, world_gross, href, mpaa_rating ) values ("' 
                    +  movie["movies"].encode("ascii","ignore").decode("ascii") + '", "' + release_date
         + '", ' +  movie["budget"][2:].replace("$", "" ).replace(",", "")  
         + ', ' +  movie["dom_gross"][2:].replace("$", "" ).replace(",", "")  
         + ', ' +  movie["world_gross"][2:].replace("$", "" ).replace(",", "")   
         + ', "' + movie["href"] [:100]
         + '", "' + mpaa_rating + '" ) ' )
    
    #except :
     #   print(movie)
    
                                                       
conn.commit()
				
cur.close()
conn.close()