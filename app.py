from flask import Flask, render_template,request,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudapp'
 
mysql = MySQL(app)


@app.route("/")
@app.route("/index", methods=['GET','POST'])
def index():

   cursor = mysql.connection.cursor()
   cursor.execute("SELECT * FROM crud")
   data = cursor.fetchall()
   cursor.close()


   if request.method == 'POST':
      id = request.form["id"]
      name = request.form["name"]
      email = request.form["email"]
      phone = request.form["phone"]
      cursor = mysql.connection.cursor()
      cursor.execute("INSERT INTO crud VALUES (%s, %s, %s, %s)", (id,name,email,phone))
      mysql.connection.commit()
      cursor.close()
   return render_template("index.html", crud = data)

@app.route("/update", methods=['GET','POST'])
def update():
   if request.method== 'POST':
      id = request.form["id"]
      name = request.form["name"]
      email = request.form["email"]
      phone = request.form["phone"]
      cursor = mysql.connection.cursor()
      cursor.execute("UPDATE crud SET name = %s, email = %s, phone = %s WHERE id = %s", (name,email,phone,id))
      mysql.connection.commit()
      cursor.close()

   return redirect(url_for("index"))  

@app.route("/delete/<string:id>", methods=['GET','POST'])
def delete(id):

   cursor = mysql.connection.cursor()
   cursor.execute("DELETE FROM crud WHERE id = %s", (id))
   mysql.connection.commit()

   return redirect(url_for("index"))  

if __name__ == '__main__':
   app.run()