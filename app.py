from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initiated Flask, SQLAlchemy, and the Database.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Created database model
class Todo(db.Model):
    '''This model creates a table with 3 columns; id, content, and date.'''
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        '''This function returns the id'''
        return "<Task %r>" % self.id

# Defining app route for index
# Methods are included since the option to post is available.
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Takes the content from the HTML page for id=content and 
        #  assigns it to local var
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            # Adds new content to the DB
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your task"

    else:
        # If there is no POST request, then the page instead lists all current tasks by date created.
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)

# Defning app route with dynamic id var and passing it to the function
@app.route('/delete/<int:id>')
def delete(id):
    '''Finds the matching id in the DB and deletes it.'''
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting the task."

# Defning app route with dynamic id var and passing it to the function
# Methods are included since the option to post is available.
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    '''Finds matching ID and replaces new content to the current one.'''
    task_to_update = Todo.query.get_or_404(id)

    if request.method == "POST":
        task_to_update.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating the task."
    else:
        return render_template('update.html', task=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)