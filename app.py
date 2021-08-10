from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'kkroot'
app.config['MYSQL_PASSWORD'] = 'k6415dl'
app.config['MYSQL_HOST'] = 'devdb.maniapc.org'
app.config['MYSQL_DB'] = 'megalan_dev'
app.config['MYSQL_PORT'] = 3307

headings = ("№ поръчка", "Статус", "Клиент", "Приета на", "Приета от", "Приета в", "Сума", "Плащане",
"Доставка на", "Доставена", "Град", "Адрес", "Адрес на доставка", "Мобилен", "Брой доставки", "Бележки")

base_sql_statement = '''SELECT o.id, s.name AS status_text, c.name AS client_name,
  CONVERT(DATE_FORMAT(o.createdon, "%Y-%m-%d %H:%i"), DATETIME) AS create_date, u.name AS create_user, c1.name AS create_club,
  #IF(o.status IN (3,4,7), c2.name, NULL) AS paid_club,
  o.total, p.mlpaytype_name, o.deliveryon, o.delivered,c.town, c.address, c.dlvry_address, c.mobile,
  CONVERT(IF(YEAR(o.deliveryon)<=2000, NULL, DAYOFYEAR(o.deliveryon) - DAYOFYEAR(NOW())), SIGNED) AS dlvry_cnt,
  o.order_note
FROM orders o LEFT JOIN order_status s ON (s.id=o.status)
  LEFT JOIN clients c ON (c.client_id=o.client_id)      LEFT JOIN users u ON (u.user_id=o.createdby)
  LEFT JOIN firm_club c1 ON (c1.club_id=o.create_club)  LEFT JOIN firm_club c2 ON (c2.club_id=o.paid_club)
  LEFT JOIN users u1 ON(u1.user_id=o.dealer_id)
  LEFT JOIN megalan_paytypes p ON (p.mlpaytype_id = o.mlpaytype_id)
WHERE(o.delivery>0)AND(o.createdon>=DATE_ADD(NOW(), INTERVAL -12 MONTH))AND(o.status IN (0,1,2,3,4,7))
AND(o.delivered=0)'''

@app.route("/")
def table():
    cur = mysql.connection.cursor()
    cur.execute(base_sql_statement)
    res = cur.fetchall()
    return render_template("table.html", headings=headings, data=res)
    
@app.route("/order/<int:id>")
def order(id):
    cur = mysql.connection.cursor()
    current_statement = base_sql_statement + "AND o.id = {}".format(id)
    cur.execute(current_statement)
    res = cur.fetchall()
    #res.fileldbyname('client_name')... 
    return render_template("order.html", data=res)

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)