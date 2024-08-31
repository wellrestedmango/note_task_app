from unicodedata import category

from docutils.nodes import description
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']=\
#    'sqlite:///' + os.path.join(basedir, 'database.db')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#to create or change do the following
#in terminal export FLASK_APP=app
#flask shell
#from app import db, Task
#db.create_all() to create
#db.drop_all() if you need to drop and restart


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    due = db.Column(db.String(50), nullable=True)
    complete = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return "<Task(title='%s', description='%s', complete='%s', category='%s')>" % (
            self.title,
            self.description,
            self.complete,
            self.category
        )







@app.route('/', methods=['POST', 'GET'])
def landing():
    if request.method == 'POST':
        task_title = request.form['title']
        task_description = request.form['description']
        task_due = request.form['due-date']
        task_category = request.form['task-category']
        new_task = Task(
            title = task_title,
            description = task_description,
            category = task_category,
            due = task_due
        )

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue adding this task. Please reload'

    else:
        task_list = Task.query.all()
        return render_template('index.html', task_list=task_list)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'failed to delete'

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)