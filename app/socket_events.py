from flask import request
from flask_socketio import join_room, leave_room, emit
from app import socketio, db
from app.models import User, Chats

@socketio.on("join_room")
def join(data):
    check = User.query.filter_by(username=data['username'], room_id=data['room']).first()
    if not check:
        user = User(username=data['username'], room_id=data['room'])
        db.session.add(user)
        db.session.commit()
    room = data['room']
    history_msg = Chats.query.filter_by(room_id = room).order_by(Chats.timestamp).limit(50).all()
    messages = [{'username': ele.username, "content":  ele.content} for ele in history_msg]
    socketio.emit("messages", messages, to = request.sid)

    join_room(data['room'])
    socketio.emit("join_announcement", data, to=data['room'])

@socketio.on("send_msg")
def send_msg(data):
    msg = Chats(room_id=data['room'], content=data['message'], username=data['username'])
    db.session.add(msg)
    db.session.commit()
    socketio.emit("receive_msg", data, to=data['room'])

@socketio.on("leave")
def leave(data):
    leave_room(data['room'])
    socketio.emit("leave_annoucement", data, to=data['room'])