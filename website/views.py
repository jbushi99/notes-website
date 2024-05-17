from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, User, Following, Message
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_text = request.form.get('note')

        if len(note_text) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(note_text=note_text, note_user_id=current_user.user_id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    following = db.session.query(User, Following).filter(Following.user_id2==User.user_id).filter(Following.user_id==current_user.user_id).all()
    followers = db.session.query(User, Following).filter(Following.user_id==User.user_id).filter(Following.user_id2==current_user.user_id).all()
    #print(followed_people[0][0].user_username)
    #print(current_user.user_following.user_id)
    following = [i[0].user_username for i in following]
    followers = [i[0].user_username for i in followers]
    return render_template("home.html", user=current_user, following=following, followers=followers)

@views.route('/inbox', methods=['GET'])
@login_required
def inbox():
    return render_template("inbox.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.note_user_id == current_user.user_id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/delete-message', methods=['POST'])
def delete_message():
    message = json.loads(request.data)
    messageId = message['messageId']
    message = Message.query.get(messageId)
    if message:
        if message.message_user_id == current_user.user_id:
            db.session.delete(message)
            db.session.commit()
    return jsonify({})

@views.route('/update-note-status', methods=['POST'])
def update_note_status():
    update = json.loads(request.data)
    noteId = update['noteId']
    status = update['status']
    '''if(status == 1):
        status = 'private'
    elif(status == 2):
        status = 'friends'
    else:
        status = 'public' '''
    note = Note.query.get(noteId)
    if note:
        if note.note_user_id == current_user.user_id:
            note.note_visibility = status
            db.session.commit()
    return jsonify({})

@views.route('/others/<user_name>', methods=['GET', 'POST'])
@login_required
def view_other(user_name):
    otheruser = User.query.filter_by(user_username=str(user_name)).first()
    if not otheruser:
        flash('User not found!', category='info')
        return home()
    elif otheruser.user_id == current_user.user_id:
        flash('It is you!', category='info')
        return home()
    else:
        if request.method == 'POST':
            message_text = request.form.get('message')
            if len(message_text) < 1:
                flash('Message is too short!', category='error')
            else:
                new_message = Message(message_text=message_text, from_user_id=current_user.user_id, message_user_id=otheruser.user_id)
                db.session.add(new_message)
                db.session.commit()
                flash('Message sent!', category='success')
        
        if otheruser.user_id in [i.user_id2 for i in current_user.user_following]:
            is_following = True
            followButtonText = "UNFOLLOW"
        else:
            is_following = False
            followButtonText = "FOLLOW"
        return render_template("others.html", user=current_user, otheruser=otheruser, is_following=is_following, followButtonText=followButtonText)
    
@views.route('/add-friend', methods=['POST'])
def add_friend():
    friend = json.loads(request.data)
    friendID = friend['user_id2']
    new_friendship = Following(user_id2=friendID, user_id=current_user.user_id)
    db.session.add(new_friendship)
    db.session.commit()
    flash('Followed!', category='success')
    return jsonify({})

@views.route('/delete-friend', methods=['POST'])
def delete_friend():
    old_friendship = json.loads(request.data)
    user_id2 = old_friendship['user_id2']
    old_friendship = Following.query.filter_by(user_id2=user_id2).first()
    db.session.delete(old_friendship)
    db.session.commit()
    flash('Unfollowed!', category='success')
    return jsonify({})