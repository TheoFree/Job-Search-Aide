from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
import re, datetime
from dbAccessConfig import db_credentials 
app = Flask(__name__)

app.config['MYSQL_USER'] = db_credentials["user"]
app.config['MYSQL_PASSWORD'] = db_credentials["password"]
app.config['MYSQL_DB'] = db_credentials["Database"]
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
CORS(app)
# print("Made it here")

@app.route('/articles/<category>/<genre>/list',methods=['Get'])
def get_articles_wPages(category,genre):
    cur = mysql.connection.cursor()
    cur.execute("SELECT count(*) FROM articles WHERE category = '{}' AND genre = '{}' ".format(genre,category))
    countArticles = cur.fetchall()
    if 'pg' in request.args:
        pgNum = request.args.get('pg', '')
        print('got it',pgNum)
        if 'ord' in request.args:
            order = request.args.get('ord',)
            cur.execute('''SELECT * FROM articles WHERE category = '{}' AND genre = '{}' ORDER BY dateposted {} LIMIT 20 OFFSET {} '''.format(category,genre,order,pgNum) )
        else:
            cur.execute('''SELECT * FROM articles WHERE category = '{}' AND genre = '{}' ORDER BY dateposted DESC LIMIT 20 OFFSET {} '''.format(category,genre,pgNum) )
    else:
        cur.execute('''SELECT * FROM articles WHERE category = '{}' AND genre = '{}' ORDER BY dateposted DESC '''.format(category,genre))
    rv = cur.fetchall()
    return jsonify({'articles':rv,'count':countArticles})

@app.route('/articles/<category>/<genre>/search',methods=['Get'])
def search_articles(category,genre):
    if 'q' in request.args:
        query = request.args.get('q',)
        cur = mysql.connection.cursor()
        count = 0
        if re.search('.+\s.+',query)!=None:
            terms = query.split()
            sqlString = '''
                SELECT DISTINCT *
                FROM articles
                WHERE 
                    (category = '{}' AND genre = '{}') AND
                    ((LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%'))''' 
            for word in terms:
                
                sqlString = sqlString + ''' OR  (LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%'))'''
            sqlString = sqlString + '''
                    )'''
            endstr='''
               ORDER BY dateposted
                {}
                LIMIT 20
                OFFSET {}
            '''
            print(sqlString)
            print((terms+[query]))
            #print(sqlString.format(genre,query,*terms ,request.args.get('ord'),request.args.get('pg',)))
            cur.execute(sqlString.format(category,genre,query,*terms))
            count = cur.rowcount
            cur.execute((sqlString+endstr).format(category,genre,query,*terms,request.args.get('ord'),request.args.get('pg',)))
            return jsonify({'articles':cur.fetchall(),'count':count})
        if '&' in query:
            terms = query.split('&')
            sqlString = '''
                SELECT *
                FROM articles
                WHERE 
                    (category = '{}' AND genre = '{}') AND
                    ((LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%')) OR (''' 
            for i in range(0,len(terms)):
                if(i==0):
                    sqlString = sqlString + '''(LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%'))'''
                else:
                    sqlString = sqlString + ''' AND  (LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%'))'''
            sqlString = sqlString + '''
                    ))
            '''
            endstr = '''
                ORDER BY dateposted
                {}
                LIMIT 20
                OFFSET {}
            '''
            print(sqlString)
            print((terms+[query]))
            #print(sqlString.format(genre,query,*terms ,request.args.get('ord'),request.args.get('pg',)))
            cur.execute(sqlString.format(category,genre,query,*terms))
            count = cur.rowcount
            cur.execute((sqlString+endstr).format(category,genre,query,*terms,request.args.get('ord'),request.args.get('pg',)))
            return jsonify({'articles':cur.fetchall(),'count':count})
        else:
            print('else')
            cur.execute('''
                SELECT DISTINCT title
                FROM articles
                WHERE 
                    (category = '{}' AND genre = '{}') AND
                    LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%')'''.format(category,genre,request.args.get('q',)))
            count = cur.rowcount
            cur.execute('''
                SELECT *
                FROM articles
                WHERE 
                    (category = '{}' AND genre = '{}') AND
                    LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%')
                ORDER BY dateposted
                {}
                LIMIT 20
                OFFSET {}
            '''.format(category,genre,request.args.get('q',),request.args.get('ord'),request.args.get('pg',)))
            return jsonify({'articles':cur.fetchall(),'count':count})

@app.route('/sources/genres',methods=['Get'])
def get_source_genres():
    cur = mysql.connection.cursor()
    res = []
    cur.execute('SELECT DISTINCT category FROM sources')
    cats = cur.fetchall()
    # temp = []
    for cat in cats:
        temp = [cat[0]]
        # print(cat[0])
        cur.execute('''SELECT DISTINCT genre FROM sources WHERE category = '{}' '''.format(cat[0]))
        temp.append(cur.fetchall())
        res.append(temp)
    return jsonify(res)
@app.route('/sources/',methods=['Get'])
def get_sources():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM sources')
    res = cur.fetchall()
    # print(res)
    return jsonify([res])

@app.route('/sources/add/<url>&<params>&<date>&<cat>&<genre>',methods = ['POST'])
def new_source(url,params,date,cat,genre):
    cur = mysql.connection.cursor()

    cur.execute('''
    INSERT
    INTO sources (url,params,lastchecked,category,genre) 
    VALUES ('{}','{}','{}','{}','{}')'''.format(url,params,datetime.datetime.now(),cat,genre))
    # print(cur.fetchall())

    mysql.connection.commit()
    get_sources()
    return(jsonify(cur.fetchall()))
@app.route('/sources/delete/<id>',methods = ['DELETE'])
def removeSource(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM sources WHERE idsources = '{}' ".format(id))
    print('removed ',id)
    mysql.connection.commit()
    get_sources()
    return(jsonify(cur.fetchall()))
if __name__ == '__main__':
    app.run(debug=True ) 