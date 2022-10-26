from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string


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

def get_random_url():
    letters = string.ascii_lowercase
    result_url = ''.join(random.choice(letters) for i in range(4))
    url_already_exists = Urls.query.filter_by(small_url=result_url).first()
    while url_already_exists:
        result_url = ''.join(random.choice(letters) for i in range(4))
        url_already_exists = Urls.query.filter_by(small_url=result_url).first()
    return result_url 


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("home.html", display="none")
    elif request.method == "POST":
        url_to_squash = request.form["url_to_squash"]
        existing_squashed_url = Urls.query.filter_by(big_url=url_to_squash).first()
        if existing_squashed_url:
            return render_template("home.html", url=existing_squashed_url.small_url)
        else:
            random_url = get_random_url()
            new_squashed_url = Urls(url_to_squash, random_url)
            db.session.add(new_squashed_url)
            db.session.commit()
            return render_template("home.html", url=f"http://localhost:5000/{random_url}") 

@app.route("/<small_url>")
def go_to_page(small_url):
    stored_urls = Urls.query.filter_by(small_url=small_url).first()
    if stored_urls:
        return redirect(stored_urls.big_url)
    else:
        return f"Url doesn`t exist"

if __name__ == "__main__":
    app.run(debug=True)

