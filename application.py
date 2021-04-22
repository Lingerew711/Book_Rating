from flask import Flask, render_template, request, session, logging, url_for,redirect,flash, jsonify
from sqlalchemy import create_engine
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt

import hashlib
import os
import requests

engine = create_engine("postgresql://postgres:linge531@localhost:5432/Book_store")

db=scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

#password hashing

def password_hash(password):
    salt = "27a0091dee99016f8fb6599da096feff"
    slat_password = password+salt
    hashed_password = hashlib.md5(slat_password.encode())
    return hashed_password.hexdigest()

#goodreads data

def get_goodreads_data(isbn):
    response = requests.get("https://www.goodreads.com/book/review_counts.json", params={ "isbns": isbn})
    value = response.json().get('books')[0]
    count = value.get('work_ratings_count')
    rating = value.get('average_rating')
    return [count,rating]

#review statistics
def get_review_statistics(book_id):
    res = db.execute("SELECT count(review),round(avg(rating),2) FROM reviews where book_id=:id;",{'id':book_id}).fetchone()
    return [res.count,float(str(res.round))]



#Index route
@app.route("/")
def search():
    return render_template('search.html')

#registration form
@app.route('/register', methods = ["GET", "POST"])
def register():
    isbn = request.args.get('next')
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1!=password2:
            return render_template('signup.html',message="Password did not match.")
           
        try:
            password = password_hash(password1)
            user = db.execute("insert into users (name,username,password) values(:name, :username ,:password);",{'name':name,'username':username,'password':password})
            db.commit()
            session['logged_in'] = True
            session['username'] = username
            if isbn:
                return redirect(url_for("book",isbn=isbn))
            return redirect(url_for("search"))
        except:
            return render_template('signup.html',message="Username Exists. Try Another.")
    return render_template('signup.html',next=isbn)

