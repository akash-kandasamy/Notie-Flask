from flask import Flask,render_template,url_for,request,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
db = SQLAlchemy(app)
dbTodo = SQLAlchemy(app)

class Todo(dbTodo.Model):
    id = dbTodo.Column(db.Integer,primary_key=True)
    content = dbTodo.Column(db.String(200),nullable=False)
    BlockId = dbTodo.Column(db.Integer)

class Blocks(db.Model):
    id = db.Column(db.Integer,primary_key=True);
    date_create = db.Column(db.DateTime,default=datetime.utcnow)

@app.route('/',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        Block = Blocks()
        db.session.add(Block)
        db.session.commit()
        all_blocks = Blocks.query.order_by(Blocks.date_create).all()
        return redirect('/')
    else:
        all_blocks = Blocks.query.order_by(Blocks.date_create).all()
        return render_template('home.html',all_blocks=all_blocks)

@app.route('/addto/<int:id>',methods=['POST'])
def addto(id):
    if request.method == 'POST':
        todo = Todo(content=request.form['content'],blockId=id)
        dbTodo.session.add(todo)
        dbTodo.session.commit()
        print(Blocks.query.order_by(Blocks.date_create).all())
        return redirect('/')
    else:
        print(Blocks.query.order_by(Blocks.date_create).all())
        return "failed"


if __name__ == "__main__":
    app.run(debug=True)
