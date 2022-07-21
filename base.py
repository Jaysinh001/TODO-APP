from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo_list(db.Model):
    srno = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(200) , nullable=False)
    description = db.Column(db.String(500) , nullable=True)
    complete = db.Column(db.Boolean)     
    date = db.Column(db.DateTime , default=datetime.now)


# @app.route("/", methods = ['GET', 'POST'])
# def home():
#     if (request.method=='POST'):
#         '''Add entry to the database'''
#         title = request.form.get('title')
#         description = request.form.get('description')

#         entry = Todo_list(title=title, description = description , date= datetime.now())
#         db.session.add(entry)
#         db.session.commit()

#     return render_template("index.html", todo_items = entry)


@app.route('/')
def index():
    # show all list of TODOs
    todo_list = Todo_list.query.all()
    return render_template("index.html", todo_list = todo_list)

@app.route('/add' , methods = ['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    entry = Todo_list(title=title, description = description , date= datetime.now() , complete = False)
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_srno>')
def update(todo_srno):
    todo = Todo_list.query.filter_by(srno = todo_srno).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:todo_srno>')
def delete(todo_srno):
    todo = Todo_list.query.filter_by(srno = todo_srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))




if __name__ == "__main__":

    db.create_all()

    # new_todo = Todo_list(title= 'Todo 1' , description = 'First Todo Item', complete = False , date = datetime.now())
    # db.session.add(new_todo)
    # db.session.commit()

    app.run(debug=True)