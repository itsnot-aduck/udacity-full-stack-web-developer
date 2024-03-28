# Run command: python3 -m flask --app .\01-connecting-to-database.py run

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Intialize the instance of SQLAlchemy
db = SQLAlchemy(app)
app.app_context().push()

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)

# Detect modules and creates tables for them (if they don't exist)
db.create_all()

@app.route('/')
def index():
    person = Person.query.first()
    return 'Hello ' + person.name