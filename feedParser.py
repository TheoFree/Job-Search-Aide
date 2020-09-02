from bs4 import BeautifulSoup as bs
import feedparser, html, requests, mysql.connector, datetime , re


#connect to database 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Cathars|s13",
    database="pywebscrapperdb"
)
#select statement -> get all from sources table to send html requests to.
cursor = db.cursor()
cursor.execute("SELECT * FROM sources")
res = cursor.fetchall()

#get datetime from last check, to make sure that it stays up to date
oldTime = res[0][3]  
sql = "UPDATE sources SET lastchecked = '{}' WHERE (lastchecked = '{}') & (idsources > 0)"
time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S")
query = sql.format(time,oldTime)
cursor.execute(query)
#update all sources with fresh query datetime
db.commit()
print(cursor.rowcount,"record(s) affected")
url=res[0][1]
params=res[0][2]
r=requests.get(url,params)
#send out html request to retrieved url with params for tuned search results, proceed if response is good.
if(r.status_code == requests.codes.ok):
    print("got it")
    document = bs(r.text,'html.parser')
        # with open("new.html","w", encoding="utf-8") as f:
    #     f.write(document.prettify())
    #     f.close()
    
    articles = document.find('div',id="main").find_all('div',class_="item-post excerpt-video")
    # article_headers = main.find_all('h4')
    # article_dates = main.find_all('span',class_='date')
    # article_authors = main.find_all('span',class_='author')
    # article_contents = main.find_all('div',class_="entry-excerpt")
    entries = []
    longestLink = 0
    for article in articles:
        entries.append(
            (
                article.find('h4').text.strip(),#title
                article.find('span',class_='date').text.strip(), #date
                article.find('span',class_='author').text.strip(), #author
                article.find('p').text.strip(), #excerpt/article preview
                article.find('div',class_='entry-excerpt').find('a').get('href').strip() #full article link
            )
        )
        temp = len(article.find('p').text.strip())
        if( temp > longestLink): longestLink = temp
    print(longestLink)
    print("entries generated")
    upload_sql = "INSERT INTO articles (title,dateposted,author,content,source) VALUES (%s,%s,%s,%s,%s);"
    upload_vals = entries
    cursor.executemany(upload_sql,entries)
    db.commit()
    print(cursor.rowcount,"record(s) affected")
