from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy()
db.init_app(app)

class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    avatar_url = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/trainer')
def trainer():
    return render_template("trainer.html")

@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        trainer_name = request.form['name']
        trainer_avatar_url = request.form['avatar_url']
        trainer_description = request.form['description']
        new_trainer = Trainer(name=trainer_name, avatar_url=trainer_avatar_url, description=trainer_description)
        
        try:
            db.session.add(new_trainer)
            db.session.commit()
            return redirect('/trainers')
        except:
            return 'There was an issue signing up'

    else: 
        return render_template('sign-in.html')


@app.route("/Database")
def trainers():
    trainers = Trainer.query.order_by(Trainer.date_created).all()
    print(len(trainers))
    return render_template('Database.html', trainers=trainers)


if (__name__ == "__main__"):
    app.run(debug=True)

