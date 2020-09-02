####### Web Scraper Design #######

Py libraries : 
    requests (HTTP) 
    BeautifulSoup (Parse/Scrape content from sites)
    celery or apscheduler (running scraper as bg process) <=- not being used yet

Uses MySql Database with two tables to collect data. 
    ->Sources Table stores websites which will be scraped
    ->Articles Table stores information from those sites for individual articles. 

Create a website that will display content?
