from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
import re
app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Cathars|s13'
app.config['MYSQL_DB'] = 'pywebscrapperdb'

mysql = MySQL(app)
CORS(app)
# print("Made it here")

@app.route('/articles/<genre>/list',methods=['Get'])
def get_articles_wPages(genre):
    cur = mysql.connection.cursor()
    cur.execute("SELECT count(*) FROM articles WHERE genre = '{}' ".format(genre))
    countArticles = cur.fetchall()
    if 'pg' in request.args:
        pgNum = request.args.get('pg', '')
        print('got it',pgNum)
        if 'ord' in request.args:
            order = request.args.get('ord',)
            cur.execute('''SELECT * FROM articles WHERE genre = '{}' ORDER BY dateposted {} LIMIT 20 OFFSET {} '''.format(genre,order,pgNum) )
        else:
            cur.execute('''SELECT * FROM articles WHERE genre = '{}' ORDER BY dateposted DESC LIMIT 20 OFFSET {} '''.format(genre,pgNum) )
    else:
        cur.execute('''SELECT * FROM articles WHERE genre = '%s' ORDER BY dateposted DESC '''%genre)
    rv = cur.fetchall()
    return jsonify({'articles':rv,'count':countArticles})

@app.route('/articles/<genre>/search',methods=['Get'])
def search_articles(genre):
    if 'q' in request.args:
        query = request.args.get('q',)
        cur = mysql.connection.cursor()

        if re.search('.+\s.+',query)!=None:
            terms = query.split()
            sqlString = '''
                SELECT *
                FROM articles
                WHERE 
                    genre = '{}' AND
                    ((LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%'))''' 
            for word in terms:
                
                sqlString = sqlString + ''' OR  (LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%'))'''
            sqlString = sqlString + '''
                    )
                ORDER BY dateposted
                {}
                LIMIT 20
                OFFSET {}
            '''
            print(sqlString)
            print((terms+[query]))
            #print(sqlString.format(genre,query,*terms ,request.args.get('ord'),request.args.get('pg',)))
            cur.execute(sqlString.format(genre,query,*terms ,request.args.get('ord'),request.args.get('pg',)))
            return jsonify({'articles':cur.fetchall(),'count':cur.rowcount})
        if '&' in query:
            terms = query.split('&')
            sqlString = '''
                SELECT *
                FROM articles
                WHERE 
                    genre = '{}' AND
                    ((LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%')) OR (''' 
            for i in range(0,len(terms)):
                if(i==0):
                    sqlString = sqlString + '''(LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%'))'''
                else:
                    sqlString = sqlString + ''' AND  (LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%'))'''
            sqlString = sqlString + '''
                    ))
                ORDER BY dateposted
                {}
                LIMIT 20
                OFFSET {}
            '''
            print(sqlString)
            print((terms+[query]))
            #print(sqlString.format(genre,query,*terms ,request.args.get('ord'),request.args.get('pg',)))
            cur.execute(sqlString.format(genre,query,*terms ,request.args.get('ord'),request.args.get('pg',)))
            return jsonify({'articles':cur.fetchall(),'count':cur.rowcount})
        else:
            print('else')
            cur.execute('''
                SELECT *
                FROM articles
                WHERE 
                    genre = '{}' AND
                    LOWER(CONCAT(title,'',content)) LIKE LOWER('%{}%')
                ORDER BY dateposted
                {}
                LIMIT 20
                OFFSET {}
            '''.format(genre,request.args.get('q',),request.args.get('ord'),request.args.get('pg',)))
            return jsonify({'articles':cur.fetchall(),'count':cur.rowcount})
        

if __name__ == '__main__':
    app.run(debug=True ) 