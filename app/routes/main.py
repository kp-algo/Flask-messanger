from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Customer, Rooms
from app import db

main_bp = Blueprint('main', __name__)

#home page leads to signup and login
@main_bp.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        action = request.form['button']
        if action == 'signup':
            return redirect('/signup')
        else:
            return redirect('/login')
    return render_template("index.html")

@main_bp.route('/chat', methods=['POST', 'GET'])
@login_required
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template("chat.html", username=username, room=room)
    
    return redirect('/')

@main_bp.route('/room', methods=['POST', 'GET'])
@login_required
def room():
    if request.method == "POST":
        action = request.form.get('click') #will get click
        if action == "Create":
            return redirect("/create")
        else:
            room = request.form['room']
            user = current_user.username
            return redirect(url_for('main.chat', username=user, room=room))

    return render_template("room.html")

@main_bp.route('/create', methods = ['POST', 'GET'])
@login_required
def create_room():
    if request.method == "POST":
        username = current_user.username
        room = request.form['room']
        check = Rooms.query.filter_by(room_id = room).first()
        if check:
            return "Same room exists already.", 202
        else:
            room_new = Rooms(room_id = room, memebers = 1)
            db.session.add(room_new)
            db.session.commit()
            return redirect(url_for('main.chat', username = username, room = room))
    
    return render_template('create_room.html')
