import os
#import PlayerData
from newsapi import NewsApiClient
import csv
import sqlite3
import datetime

today = datetime.datetime.now()
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)


yesterday_str = str(yesterday)[:10]
today_str = str(today)[:10]

conn = sqlite3.connect('NBA_data.db')
cur = conn.cursor()

delete_table_sql = " DROP TABLE IF EXISTS news "
create_table_sql = """ CREATE TABLE IF NOT EXISTS news(title VARCHAR, source VARCHAR, description VARCHAR, url VARCHAR, urlToImage VARCHAR, data VARCHAR);"""
news = []

newsapi = NewsApiClient(api_key='419ae5f6edad4d4a9b28a990c7af73b7')
 

print today_str
print yesterday_str

all_articles = newsapi.get_everything(q = "NBA",
                                      from_param = yesterday_str,
                                      to = today_str ,
                                      language = "en",
                                      sort_by = "relevancy",
                                      page_size = 20,
                                      page = 1)





"""    
#all_articles = newsapi.get_everything(q="nba",
                                      language='en',
                                      sort_by='publishedAt',
                                      page=1)
"""
      
news = []

for article in all_articles['articles']:

	new = []

	article_date = article['publishedAt'][:10]
	day = article_date[8:]
	month = article_date[5:7]
	year = article_date[:4]

	date = "{}-{}-{}".format(day, month, year)


	new.append(article['title'])
	new.append(article['source']['name'])
	new.append(article['description'])
	new.append(article['url'])
	new.append(article['urlToImage'])
	new.append(date)
	news.append(new)


#print news


"""
#CREARE CSV FILE

with open('nbaNews.csv','w')  as f:
      thewriter = csv.writer(f)
      for data in news:
            #print type(data)
            thewriter.writerow(data)
"""

cur.execute(delete_table_sql)
cur.execute(create_table_sql)


cur.executemany("INSERT INTO news VALUES (?,?,?,?,?,?);", news)

conn.commit()

"""
with open('nbaNews.csv', 'r') as nba_news:
	dr = csv.DictReader(nba_news)
	to_db = [()]

#creare database da csv
"""

