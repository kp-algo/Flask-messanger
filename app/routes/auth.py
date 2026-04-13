from flask import Blueprint, request, render_template, redirect
from flask_login import login_user
from flask_bcrypt import Bcrypt
from app.models import Customer
from app import db, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        check = Customer.query.filter_by(username=username).first()
        
        if not check:
            return redirect("/signup")
        else:
            if bcrypt.check_password_hash(check.password, password):
                login_user(check) 
                return redirect("/room")
            else:
                return "Kindly check your password"
                
    return render_template("login.html")

@auth_bp.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        check = Customer.query.filter_by(username=username).first()
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        if check:
            return "Name should be unique"
        else:
            customer = Customer(username=username, password=pw_hash)
            db.session.add(customer)
            db.session.commit()
            return redirect('/login')

    return render_template("signup.html")