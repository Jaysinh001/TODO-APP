from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/todo_list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




class Todo_list(db.Model):
    srno = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(200) , nullable=False)
    description = db.Column(db.String(500) , nullable=True)     
    date = db.Column(db.DateTime , default=datetime.now)



@app.route("/", methods = ['GET', 'POST'])
def home():
    if (request.method=='POST'):
        '''Add entry to the database'''
        title = request.form.get('title')
        description = request.form.get('description')

        entry = Todo_list(title=title, description = description , date= datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template("index.html", todo_items = entry)


if __name__ == "__main__":

    app.run(debug=True)