
from flask import Flask, render_template, request, redirect, flash
import pymysql

app = Flask(__name__)


def connection():
    host = 'localhost'  # Your server(host) name
    db = 'py_crud'
    user = 'root'  # Your login user
    password = ''  # Your login password
    conn = pymysql.connect(host=host, user=user, password=password, database=db)
    return conn


@app.route("/")
def main():
    cars = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tblcars")
    for row in cursor.fetchall():
        cars.append(
            {
            "id": row[0],
            "name": row[1],
            "year": row[2],
            "price": row[3]
        }
        )
    
    return render_template("carslist.html", cars=cars)

@app.route("/addcar", methods = ['GET','POST'])
def addcar():
    if request.method == 'GET':
        return render_template("addcar.html")
    if request.method == 'POST':
        name = request.form["name"]
        year = int(request.form["year"])
        price = float(request.form["price"])
        
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TblCars (name, year, price) VALUES ( %s, %s, %s)", (name, year, price))
        conn.commit()
        conn.close()
        return redirect('/')

@app.route('/update/<int:id>',methods =['GET','POST'])
def update(id):
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        car = []
        cursor.execute("SELECT * FROM tblcars WHERE id=%s",(id))
        result = cursor.fetchall()
        for row in result:
            car.append({
                'id':row[0],
                'name':row[1],
                'year':row[2],
                'price':row[3],
            })
        conn.close()
        return render_template('update.html',car = car[0])
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        price = request.form['price']
        cursor.execute("UPDATE tblcars SET name=%s, year=%s, price=%s WHERE id=%s",(name,year,price,id))
        conn.commit()
        conn.close()
        flash('Record updated')
        return redirect('/')
    
@app.route('/delete/<int:id>')
def delete(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tblcars WHERE id=%s",(id))
    conn.commit()
    conn.close()
    return redirect('/')





if(__name__ == "__main__"):
    app.run(debug=True)
