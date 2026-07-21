import psycopg2, secrets
from flask import Flask, render_template, request, session
from datetime import datetime

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

@app.route('/ticket', methods = ['POST'])
def ticket_page():
    if request.method == 'POST':
        if 'buy-departure' in request.form:
            departure = request.form['buy-departure']
            destination = request.form['buy-destination']
            cursor.execute(f"SELECT * FROM flights WHERE arrival_state = '{destination}' AND departure_state = '{departure}'")
            flight_match = cursor.fetchall()
            flight_object = {"departure": flight_match[0][1], 
                             "destination": flight_match[0][2], 
                             "departure_time": flight_match[0][3].strftime("%Y-%m-%d %H:%M"), 
                             "arrival_time": flight_match[0][4].strftime("%Y-%m-%d %H:%M"),
                             "price": flight_match[0][5]}
            return render_template('ticket.html', available_flights = flight_object, action = 'buy')

app.run()
