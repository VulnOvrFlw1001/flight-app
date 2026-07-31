import psycopg2, secrets, random, string, os
from flask import Flask, render_template, request, session
from datetime import datetime


conn =  psycopg2.connect(database=os.environ['POSTGRES_DB'],user=os.environ['POSTGRES_USER'],password=os.environ['POSTGRES_PASSWORD'],host=os.environ['POSTGRES_HOST'],port="5432")
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/', methods = ['POST','GET'])
def sign_up_page():
    return render_template('sign-up.html')
  
@app.route('/sign-in', methods = ['POST','GET'])
def sign_in_page():
  return render_template("sign-in.html")

@app.route('/shop', methods = ['POST'])
def shop_page():
    if request.method == 'POST':
        if request.referrer == "https://flight-app.flightsnotfeelings.shop/":
            email = request.form['email']
            session['username'] = request.form['username']
            password = request.form['password']
            cursor.execute(f"INSERT INTO users (name,password,email) VALUES ('{session['username']}','{password}','{email}')")
            conn.commit()
            return render_template('shop.html', name = session['username'])
        elif request.referrer == "https://flight-app.flightsnotfeelings.shop/sign-in": 
            session['username'] = request.form['username']
            password = request.form['password']
            cursor.execute(f"SELECT password FROM users where name = '{session['username']}'")
            real_password = cursor.fetchall()
            if real_password[0][0] == password:
                cursor.execute(f"SELECT departure,arrival,departure_time,arrival_time FROM tickets WHERE users = '{session['username']}'")
                user_existing_flights = cursor.fetchall()
                return render_template('shop.html', name = session['username'], flights = user_existing_flights)
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
            flight_object = {"departure": flight_match[0][1], "destination": flight_match[0][2], "departure_time": flight_match[0][3].strftime("%Y-%m-%d %H:%M"), "arrival_time": flight_match[0][4].strftime("%Y-%m-%d %H:%M"), "price": flight_match[0][5]}
            return render_template('ticket.html', available_flights = flight_object, action = 'buy')
        elif 'delete-departure' in request.form:
           session['delete-departure'] = request.form['delete-departure']
           session['delete-destination'] = request.form['delete-destination']
           cursor.execute(f"SELECT * FROM tickets WHERE arrival = '{session['delete-destination']}' AND departure = '{session['delete-departure']}' AND users = '{session['username']}'")
           flight_match = cursor.fetchall()
           return render_template('ticket.html', flight = flight_match, action = 'delete')

@app.route('/payment', methods = ['POST'])
def purchase_page():
    if request.method == 'POST':
      session['user_departure'] = request.form['departure']
      session['user_destination'] = request.form['destination']
      session['user_departure_time'] = request.form['departure_time']
      session['user_arrival_time'] = request.form['arrival_time']
      session['user_price'] = request.form['price']
      return render_template('payment.html')
  
def generate_ticket_id():
    length = 10
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/success", methods = ['POST'])
def success_page():
    if request.method == 'POST':
        ticket_id = generate_ticket_id()
        cursor.execute(f"INSERT INTO tickets (ticket_number,departure,arrival,departure_time,arrival_time,ticket_price,users) VALUES ('{ticket_id}','{session['user_departure']}','{session['user_destination']}','{session['user_departure_time']}','{session['user_arrival_time']}','{session['user_price']}','{session['username']}')")
        conn.commit()
        return render_template("success.html", ticket_id = ticket_id)

@app.route('/delete', methods = ['POST'])
def delete_page():
    if request.method == 'POST':
        cursor.execute(f"SELECT ticket_number FROM tickets WHERE arrival = '{session['delete-destination']}' AND departure = '{session['delete-departure']}' AND users = '{session['username']}'")
        correct_ticket_id = cursor.fetchall()
        ticket_id = request.form['delete-ticket-id']
        if correct_ticket_id[0][0] == ticket_id:
            cursor.execute(f"DELETE FROM tickets WHERE ticket_number = '{ticket_id}'")
            conn.commit()
            return render_template('delete.html')
        else:
            return render_template('wrong.html')
app.run(host="0.0.0.0")

