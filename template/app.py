from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Position, Voter, Candidate, Vote
from sqlalchemy import func
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'navaja-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///<yourDbName>.db'
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

if __name__ == '__main__':
    # Create instance directory if it doesn't exist
    os.makedirs('instance', exist_ok=True)

    # Initialize database
    with app.app_context():
        db.create_all()

    app.run(debug=True)
