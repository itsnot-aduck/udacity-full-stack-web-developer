from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()
migrate = Migrate(app, db)


## Model configurations
# Child model
class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False)
  list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable = False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

# Father model
class Todolist(db.Model):
  __tablename__ = 'todolists'
  id =  db.Column(db.Integer, primary_key = True, autoincrement=True)
  name = db.Column(db.String(), nullable = False)
  todos = db.relationship('Todo', backref = 'list', lazy = True)

# note: more conventionally, we would write a
# POST endpoint to /todos for the create endpoint:
# @app.route('/todos', method=['POST'])
@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    list_id = request.get_json()['list_id']
    todo = Todo(description=description)
    active_list = Todolist.query.get(list_id)
    todo.list = active_list
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    return jsonify(body)
  else:
    abort(500)

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
  return render_template('index.html',
  lists=Todolist.query.all(),
  active_list=Todolist.query.get(list_id),
  todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
)

@app.route('/')
def index():
  return redirect(url_for('get_list_todos', list_id=1))