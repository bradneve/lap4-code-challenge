from flask import Flask, render_template, request, redirect
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urlsStore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    big_url = db.Column("big_url", db.String())
    small_url = db.Column("small_url", db.String(4))

    def __init__(self, big_url, small_url):
        self.big_url = big_url
        self.small_url = small_url


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html")





if __name__ == "__main__":
    app.run(debug=True)

