from bs4 import BeautifulSoup as bs
import feedparser, html, requests, mysql.connector, datetime , re, lxml, sys

debug = False

if(len(sys.argv)>1):
    if(sys.argv[1]=='debug'): debug=True

    # if(runArg =='debug'):
    #     debug = True
    # if (runArg == 'run'):
    #     debug = False
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
# print(res)
resLength = cursor.rowcount
#get datetime from last check, to make sure that it stays up to date
oldTime = res[0][3]  
sql = "UPDATE sources SET lastchecked = '{}' WHERE (idsources > 0)"
time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S")
query = sql.format(time,oldTime)
cursor.execute(query)
delta = datetime.timedelta(10)
deadtime = datetime.date.today()-delta
deadtime = deadtime.isoformat()
print(deadtime)
cursor.execute(
    ''' DELETE 
        FROM pywebscrapperdb.articles
        WHERE ((genre = 'jobs') AND (dateposted < '{}') AND (idarticle >0))
    
    '''.format(deadtime)
)
#update all sources with fresh query datetime
db.commit()
def monthAsInt(month):
    monthEquivelence = [
            ('Jan',1),
            ('Feb',2),
            ('Mar',3),
            ('Apr',4),
            ('May',5),
            ('Jun',6),
            ('Jul',7),
            ('Aug',8),
            ('Sep',9),
            ('Oct',10),
            ('Nov',11),
            ('Dec',12)
    ]
    for i in monthEquivelence:
        if(month == i[0]):
            return i[1]
def getLink(article):
    if(not(article.find('link')==None)):
        # print('link')
        return article.find('link').text.strip()
    if(not(article.find('guid')==None)):
        # print('guid')
        return article.find('guid').text.strip()
    else:
        return url
print(cursor.rowcount,"record(s) affected")
for i in range(resLength):
    url=res[i][1]
    params=res[i][2]
    print(url,params)
    r=requests.get(url,params)
    # if i == 2: print(r.text)
    
    #send out html request to retrieved url with params for tuned search results, proceed if response is good.
    if(r.status_code == requests.codes.ok):
        if(url=="https://teksyndicate.com/"):
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
                        article.find('div',class_='entry-excerpt').find('a').get('href').strip(), #full article link
                        res[i][4], 
                        res[i][5]
                    )
                )
            #     temp = len(article.find('p').text.strip())
            #     if( temp > longestLink): longestLink = temp
            # print(longestLink)
            print("entries generated")
            upload_sql = "INSERT IGNORE INTO articles (title,dateposted,author,content,source,category,genre) VALUES (%s,%s,%s,%s,%s,%s,%s);"
            upload_vals = entries
            if(debug!=True):
                cursor.executemany(upload_sql,entries)
                db.commit()
                print(cursor.rowcount,' new')
        else:
            document = bs(r.text, "lxml-xml")
            # print(document)
            articles = document.find_all("item")
            
            

            entries = []
            
            for article in articles:
                date =re.search('.+\s(.+)\s(.+)\s(\d{4})' ,article.find('pubDate').text.strip())
                dateD = date.group(1)
                dateM = date.group(2)
                dateY = date.group(3)
                dateFormatted = datetime.date(int(dateY),monthAsInt(dateM),int(dateD)).isoformat()
                if((datetime.date.today()-datetime.date.fromisoformat(dateFormatted)).days < 10):
                    entries.append(
                        (
                            article.find('title').text,
                            dateFormatted,
                            article.find('description').text.strip(),
                            getLink(article),
                            res[i][4],
                            res[i][5]
                        )
                    )
                
            print("entries generated")
            # print(entries[0])
            upload_sql = "INSERT IGNORE INTO articles (title,dateposted,content,source,category,genre) VALUES (%s,%s,%s,%s,%s,%s);"
            upload_vals = entries
            if(debug!=True):
                cursor.executemany(upload_sql,entries)
                db.commit()
                print(cursor.rowcount,' new')
