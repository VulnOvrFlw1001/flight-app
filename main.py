import psycopg2, secrets
from flask import Flask, render_template, request, session

conn = psycopg2.connect(database="postgres",user="postgres",password="pass",host="localhost",port="5432")
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/', methods = ['POST', 'GET'])
def sign_up_page():
    return render_template('sign-up.html')