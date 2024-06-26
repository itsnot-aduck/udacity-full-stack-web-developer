from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create an application that gets named after the python file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

# Model to manage
class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key = True)
  description = db.Column(db.String(), nullable = False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'
  
# Create the database
db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
  description = request.form.get('description', '')
  todo = Todo(description=description)
  db.session.add(todo)
  db.session.commit()
  return redirect(url_for('index'))

# Setup a route to home page
@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.all())
  