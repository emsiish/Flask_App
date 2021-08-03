from flask import Flask, render_template
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
    cur.execute('''SELECT o.id, s.name AS status_text, c.name AS client_name,
  CONVERT(DATE_FORMAT(o.createdon, "%Y-%m-%d %H:%i"), DATETIME) AS create_date, u.name AS create_user, c1.name AS create_club,
  IF(o.status IN (3,4,7), c2.name, NULL) AS paid_club,
  IF(YEAR(o.payedon)>1990, DATE_FORMAT(o.payedon, "%Y-%m-%d %H:%i"), NULL) AS paid_date,
  o.status, o.client_id, o.total, o.parent_id, o.mldoctype_id, o.ware_id, o.object_id, o.vattype_id, o.valuta_id,
  o.mlpaytype_id, o.sys_version, o.deliveryon,  u1.name AS dealer_name ,o.delivered, c.town, c.address, 
  c.dlvry_address, c.phone, c.mobile,
  CONVERT(IF(YEAR(o.deliveryon)<=2000, NULL, DAYOFYEAR(o.deliveryon) - DAYOFYEAR(now())), SIGNED) AS dlvry_cnt
FROM orders o LEFT JOIN order_status s ON (s.id=o.status)
  LEFT JOIN clients c ON (c.client_id=o.client_id)      LEFT JOIN users u ON (u.user_id=o.createdby)
  LEFT JOIN firm_club c1 ON (c1.club_id=o.create_club)  LEFT JOIN firm_club c2 ON (c2.club_id=o.paid_club)
  LEFT JOIN users u1 ON(u1.user_id=o.dealer_id)
WHERE(o.delivery>0)AND(o.createdon>=DATE_ADD(NOW(), INTERVAL -12 MONTH))AND(o.status IN (0,1,2,3,4,7))
AND(o.delivered=0)''')
    res = cur.fetchall()
    return render_template("table.html", data=res)

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)