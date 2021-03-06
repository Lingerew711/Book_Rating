from flask import Flask, render_template, request, session, logging, url_for,redirect,flash, jsonify
from sqlalchemy import create_engine
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt

import hashlib
import os
import requests

engine = create_engine("postgresql://fhrgggnmrmrxkn:d9843ee1039f5c4b915f9e863e6bd74fabff6377b2933c78af4fde3845a2c7c6@ec2-52-21-252-142.compute-1.amazonaws.com:5432/dng8iia4pdh78")

db=scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

app.secret_key="1234567lingebookstore"
#password hashing

def password_hash(password):
    salt = "27a0091dee99016f8fb6599da096feff"
    slat_password = password+salt
    hashed_password = hashlib.md5(slat_password.encode())
    return hashed_password.hexdigest()


# Ensure responses aren't cached

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
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


#login form
@app.route('/login', methods=["GET", "POST"])
def login():
    isbn = request.args.get('next')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.execute("select * from users where username=:username and password=:password;",{'username':username,'password':password_hash(password)})
        if user.rowcount == 0:
            return render_template('login.html',message="Wrong Username or Password.")
        session['logged_in'] = True
        session['username'] = request.form['username']
        if isbn:
            return redirect(url_for("book",isbn=isbn))
        return redirect(url_for("search"))

    return render_template('login.html',next=isbn)

#books
@app.route("/books")
def books():
    q = request.args.get('search')
    if q != None:
        q = q.strip().replace("'","")
        obj_books = db.execute("select * from books where isbn LIKE ('%"+q+"%')  or lower(title) LIKE lower('%"+q+"%') or  lower(author) LIKE lower('%"+q+"%') order by year desc;").fetchall() 
        count = len(obj_books)
        if count == 0:
            return render_template('books.html',q=q,count=count,message="404 Not Found")


        
        return render_template('books.html',q=q,count=count,obj_books=obj_books)
    return render_template('books.html')

#book
@app.route("/book/<isbn>",methods=['GET','POST'])
def book(isbn):
    message = None
    error = False
    is_reviewed = False
    if request.method == "POST" and session['logged_in']:
        my_rating = request.form.get('rate')
        my_review = request.form.get('review')
        book_id = request.form.get('review_isbn')
        if my_review.strip()=="" or my_rating=="":
            message = "Invalid Review"
        else:
            db.execute("insert into reviews (username, review, rating, book_id) select :username,:review,:rating,:book_id where not exists (select * from reviews where username = :username and book_id = :book_id);",
            {
                'username': session['username'],
                'review': my_review,
                'rating':my_rating,
                'book_id': book_id    
            })
            db.commit()
            is_reviewed = True



    res = db.execute("select * from books where isbn=:isbn;",{'isbn':isbn}).fetchone() 
    if res==None:
        return render_template('book.html')
    

    reviews = db.execute("select * from reviews where book_id=:id;",{'id':res.isbn}).fetchall()
    if request.method == "GET":
        try:
            if session['logged_in']:
                check_review = db.execute("select user_id from reviews where book_id=:id and user_id=:user_id;",
            {
                'id':res.id,
                'user_id': session['id']  
            }).fetchone()
                if check_review != None:
                    is_reviewed = True
        except:
            pass
    try:
        count,rating = get_goodreads_data(isbn)
    except:
        error = True
        count,rating = 0,0
    return render_template('book.html',obj_book=res,count=count,rating=rating,reviews=reviews,message=message,is_reviewed=is_reviewed,error=error)

#apiurl
@app.route("/api/<isbn>")
def api_url(isbn):
    obj_books = db.execute("select * from books where isbn=:isbn;",{'isbn':isbn}).fetchone()
    if obj_books == None:
        return jsonify({
            "error": "Invalid isbn.",
            }),404
    try:
        count,rating = get_review_statistics(obj_books.id)
    except:
        count,rating = 0,0
    
    return jsonify({
        "title": obj_books.title,
        "author": obj_books.author,
        "year": obj_books.year,
        "isbn": obj_books.isbn,
        "review_count": count,
        "average_score": rating
    }),200

#logout
@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', message="Successfully Logout.")
if __name__ == "__main__":
    app.run(debug = True)

