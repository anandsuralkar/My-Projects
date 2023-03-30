import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
#import ssl

# setup mongo -Please provide proper mongodb host and port for local db and also uncomment client line
host = 'localhost'
port = 27017

# connect to the database & get a gridfs handle
connection = MongoClient(host, port)

#for mongo cloud
#connection = MongoClient("mongodb+srv://AnandDataBase:AnandDataBase@cluster0.qtzrb.mongodb.net/test",ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

sites = ['thetimesofindia','firstpost','indianexpress','moneycontrol']
siteurls=[["https://timesofindia.indiatimes.com/","https://timesofindia.indiatimes.com/sports","https://timesofindia.indiatimes.com/business"]
          ,["https://www.firstpost.com/","https://www.firstpost.com/category/sports","https://indianexpress.com/section/business/"]
          ,["https://indianexpress.com/","https://indianexpress.com/section/sports/","https://indianexpress.com/section/business/"]
          ,["https://www.moneycontrol.com/news/","https://www.moneycontrol.com/stocksmarketsindia/","https://www.moneycontrol.com/mutualfundindia/"]]
index = 0

#_______________________________________________________iterating through all four sites_________________________________________________________________________________
for site in sites:
    print()
    print(site)
    print()
    db = connection[site]

    urls = siteurls[index]
    if index != 3:
        col = ['news ','sports ','business ']
    else:
        col = ['news ','market ','mutual funds ']

    # create soup for all three sections by iteration
    i = 0
    for url in urls:
        print(col[i])
        
        htmldata = requests.get(url)
        soup = BeautifulSoup(htmldata.text, 'html.parser')


#______________________________________________________adding all images from all three sections into respective mongo collections_______________________________________________
 
        collection = db[col[i] + 'images']
        n = collection.ut.count_documents({})
        for item in soup.find_all('img'):
            try:
                img_url=item['src']
                alt = item['alt']
                collection.insert_one({'_id': n, 'Name' : alt, 'src' : img_url})
                #print(alt)
                n+=1

            except:
                pass
            
        for item in soup.find_all('img', class_="fp-lazy"):
            try:
                img_url=item['data-src']
                alt = item['alt']
                collection.insert_one({'_id': n, 'Name' : alt, 'src' : img_url})
                n+=1

            except:
                pass
            
        print(n," entries added to collection : ",col[i])
        

#______________________________________________________adding all the content of all three sections into respective mongo collections_______________________________________________
        collection = db[col[i]+'content']
        n = collection.ut.count_documents({})
        for item in soup.find_all('h2', class_="main-title"):
            try:
                collection.insert_one({'_id': n,'text' : item.text})
                #print(item.text)
                n+=1
            except:
                pass
            
        for item in soup.find_all('h3', class_="main-story-title"):
            try:
                collection.insert_one({'_id': n,'text' : item.text})
                #print(item.text)
                n+=1

            except:
                pass
            


            
        for item in soup.find_all('a'):
            try:
                collection.insert_one({'_id': n,'text' : item['title']})
                #print(item['title'])

            except:
                pass
            n+=1
        for item in soup.find_all('a'):
            try:
                collection.insert_one({'_id': n,'text' : item.text})
                #print(item['title'])
                n+=1

            except:
                pass
            
        print(n," entries added to collection : ",col[i])


#______________________________________________________adding all the links from all three sections into respective mongo collections_______________________________________________
        collection = db[col[i]+'links']
        n = collection.ut.count_documents({})
        for item in soup.find_all('a'):
            try:
                link = item['href']
                collection.insert_one({'_id': n, 'link' : link})
                #print(link)
                n+=1

            except:
                pass
        print(n," entries added to collection : ",col[i])
        i+=1
    print("Parsing and Data entered in respective mongo collections for site : ",site)
    index += 1
