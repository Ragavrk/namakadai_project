from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

import mysql.connector
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rithik@123'
app.config['MYSQL_DB'] = 'Arele'

mysql = MySQL(app)

cash_balance = 1000


items = {
    'pen': {'name': 'Pen', 'price': 5},
    'pencil': {'name': 'Pencil', 'price': 2},
    'eraser': {'name': 'Eraser', 'price': 1},
    'sharpener': {'name': 'Sharpener', 'price': 2},
    'geometry_box': {'name': 'Geometry Box', 'price': 10}
}


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('Select * From Sales')
    sales_data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('Select * From Purchase')
    purchase_data = cur.fetchall()
    cur.close()
    return render_template('index.html', cash_balance=cash_balance, items=items, sales_data=sales_data,purchase_data=purchase_data)

@app.route('/purchase', methods=['POST'])
def purchase():
    global cash_balance
    item_name = request.form['item']
    quantity = int(request.form['quantity'])
    item = items[item_name]
    total_cost = item['price'] * quantity
    if cash_balance >= total_cost:
        cash_balance -= total_cost

        amount = item['price'] * quantity

        cur = mysql.connection.cursor()
        cur.execute('insert into Purchase (rate,qty,amount) Values (%s,%s,%s)',(quantity,item['price'],amount))
        mysql.connection.commit()
        cur.close()



        return redirect('/')
    else:
        return "Insufficient cash balance."

@app.route('/sale', methods=['POST'])
def sale():
    global cash_balance
    item_name = request.form['item']
    quantity = int(request.form['quantity'])
    item = items[item_name]
    total_earning = item['price'] * quantity
    amount = item['price'] * quantity

    cur = mysql.connection.cursor()
    cur.execute('insert into Sales (rate,qty,amount) Values (%s,%s,%s)',(item['price'],quantity,amount))
    mysql.connection.commit()
    cur.close()
    cash_balance += total_earning
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
