from crypt import methods
from flask import Flask, redirect # The flask framework
from flask import render_template # To render web page files
from flask import url_for # To get the path of files
from flask_sqlalchemy import SQLAlchemy # For CRUD operations on the database
from flask import request # To handle HTTP requests
from datetime import datetime # For storing dates and times in the database

# The flask app
app = Flask(__name__)
# Tells SQLAlchemy where the database is located (path of the database) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# To create an SqlAlchemy database
db = SQLAlchemy(app)

# Todo relation in sqlite database
# Inherits from class Model of db
class Todo(db.Model):
    # Each variable is a column
    id = db.Column(db.Integer, primary_key = True)
    # Nullable is NOT NULL, String is VARCHAR
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    # Datetime will automatically be set to the UTC timezone
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    # Used to represent an object of class Todo as a string
    # Will return 'Task <id>' as a string
    def __repr__(self):
        return '<Task %r>' % self.id

# URL for index()
# Returns web resource (such as a web page)
# Added HTTP methods
@app.route('/', methods = ['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        # Code to do things when Add Task is pressed
        # Processes the POST requests of the form named "content"
        task_content = request.form['content']
        
        # Created an object of type Todo and
        # put the content of the form called "content"
        # in that object
        new_task = Todo(content = task_content)

        # Code to add tuples to Todo relation
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return"Error in adding item to database"
    
    else:
        # SELECT * FROM Todo ORDER BY date_created;
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Pass query output to the template
        return render_template('index.html', tasks = tasks)

# Deletion logic
@app.route('/delete/<int:id>')
def delete(id):
    # Get the task to be deleted through id
    task_to_delete = Todo.query.get_or_404(id)

    # Delete the task
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Error in deleting task"

# Updation logic
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    # Get the task to be updated by task id
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error updating task"

    else:
        return render_template('update.html', task = task)

# Main function to run the app
if __name__ == "__main__":
    # Call to run the app
    # Debugging turned on shows any errors with pages
    app.run(debug = True)