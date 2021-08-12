from flask import Flask, render_template
from flask_mysqldb import MySQL
from delivery_description import Delivery

app = Flask(__name__, instance_path="/{project_folder_abs_path}/instance")

app.config['MYSQL_USER'] = 'kkroot'
app.config['MYSQL_PASSWORD'] = 'k6415dl'
app.config['MYSQL_HOST'] = 'devdb.maniapc.org'
app.config['MYSQL_DB'] = 'megalan_dev'
app.config['MYSQL_PORT'] = 3307

headings = ("№ поръчка", "Статус", "Клиент", "Приета на", "Приета от", "Приета в", "Сума", "Плащане",
            "Доставка на", "Град", "Адрес", "Адрес на доставка", "Мобилен", "Бележки")

base_sql_statement = '''SELECT o.id, s.name AS status_text, c.name AS client_name,
  CONVERT(DATE_FORMAT(o.createdon, "%Y-%m-%d %H:%i"), DATETIME) AS create_date, u.name AS create_user, c1.name AS create_club,
  #IF(o.status IN (3,4,7), c2.name, NULL) AS paid_club,
  o.total AS order_total, p.mlpaytype_name, o.deliveryon,c.town, c.address AS client_address, c.dlvry_address, c.mobile,
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
    res = cur.fetchone()
    data = Delivery()
    data.order_id = res[0]
    data.client_name = res[2]
    data.create_date = res[3]
    data.create_user = res[4]
    data.create_club = res[5]
    data.order_total = res[6]
    data.mlpaytype_name = res[7]
    data.deliveryon = res[8]
    data.client_address = res[10]
    data.dlvry_address = res[11]
    data.mobile = res[12]
    data.order_note = res[13]

    return render_template("orders.html", data=data)


mysql = MySQL(app)

if __name__ == '__main__':
    app.run()
