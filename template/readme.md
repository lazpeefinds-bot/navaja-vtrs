in requirements.txt
You sent
pip install -r requirments.txt
You sent
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.23
You sent
npm init
You sent
in package.json
"scripts": {
    "build:css": "tailwindcss -i ./static/src/input.css -o ./static/src/output.css",
    "watch:css": "tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch",
    "test": "echo \"Error: no test specified\" && exit 1"
  }
You sent
npm install tailwindcss @tailwindcss/cli

npm run watch:css
You sent
sqlite3 instance/<dbname>.db < <dbname>.sql
17:50
You sent
in app.py: 
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Position, Voter, Candidate, Vote
from sqlalchemy import func
import os

app = Flask(_name_)
app.config['SECRET_KEY'] = 'navaja-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///election.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized!")


# Home route
@app.route('/')
def index():
    return render_template('index.html')

if _name_ == '_main_':
    # Initialize database
    with app.app_context():
        db.create_all()

    app.run(debug=True)