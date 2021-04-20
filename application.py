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

# Check for environment variable


@app.route("/")
def index():
    return render_template('layout.html')
