from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'kkroot'
app.config['MYSQL_PASSWORD'] = 'k6415dl'
app.config['MYSQL_HOST'] = 'devdb.maniapc.org'
app.config['MYSQL_DB'] = 'megalan_dev'
app.config['MYSQL_PORT'] = 3307

@app.route("/")
def hello_world():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT orders.id FROM orders WHERE id > 4000000 
    AND id < 4000100''')
    res = cur.fetchall()

    return str(res)

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)
#sdf