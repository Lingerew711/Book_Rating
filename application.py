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


# Check for environment variable


@app.route("/")
def index():
    return render_template('search.html')
