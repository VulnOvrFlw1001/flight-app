import psycopg2, secrets
from flask import Flask, render_template, request, session

conn = psycopg2.connect(database="postgres",user="postgres",password="admin",host="localhost",port="5432")
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/', methods = ['POST', 'GET'])
def sign_up_page():
    return render_template('sign-up.html')

@app.route('/sign-in', methods = ['POST', 'GET'])
def sign_in_page():
    return render_template("sign-in.html")

@app.route('/shop', methods = ['POST'])
def shop_page():
    if request.method == 'POST':
        if request.referrer == "http://localhost:5000/":
            email = request.form['email']
            session['username'] = request.form['username']
            password = request.form['password']
            cursor.execute(f"INSERT INTO users (name,password,email) VALUES ('{session['username']}','{password}','{email}')")
            conn.commit()
            return render_template('shop.html', name = session['username'])
        elif request.referrer == "http://localhost:5000/sign-in":
            session['username'] = request.form['username']
            password = request.form['password']
            cursor.execute(f"SELECT password FROM users where name = '{session['username']}'")
            real_password = cursor.fetchall()
            if real_password[0][0] == password:
                return render_template('shop.html', name = session['username'])
            else:
                return render_template('wrong.html')

app.run()
