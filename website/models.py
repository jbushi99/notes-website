from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint

class Note(db.Model):
    __tablename__ = 'note'
    note_id = db.Column(db.Integer, primary_key=True)
    note_text = db.Column(db.String(10000)) # the contents of the note
    note_date = db.Column(db.DateTime(timezone=True), default=func.now()) # the date the note was posted
    note_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id')) # id of the user who has posted the note
    note_visibility = db.Column(db.Integer, default=0) # (added) 0: private; 1: shared with friends only; 2: public
    def get_id(self):
        return (self.note_id)
    
class Message(db.Model):
    __tablename__ = 'message'
    message_id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.String(10000)) # the contents of the note
    message_date = db.Column(db.DateTime(timezone=True), default=func.now()) # the date the note was posted
    from_user_id = db.Column(db.Integer) # id of the user who sent the message
    message_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id')) # id of the user who received the message
    def get_id(self):
        return (self.message_id)

class Following(db.Model):
    __tablename__ = 'following'
    following_id = db.Column(db.Integer, primary_key=True) # not strictly necessary...
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id')) # follower
    user_id2 = db.Column(db.Integer) # following
    __table_args__ = (UniqueConstraint("user_id", "user_id2", name='follower_following'),)
    def get_id(self):
        return (self.following_id)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150), unique=True) #no user can have the same email as another user
    user_password = db.Column(db.String(150))
    user_username = db.Column(db.String(150), unique=True)
    user_notes = db.relationship('Note')
    user_messages = db.relationship('Message')
    user_isHidden = db.Column(db.Boolean, default=True) #(added) True: does not appear on search results
    user_isAuthenticated = db.Column(db.Boolean, default=False) 
    user_following = db.relationship('Following')
    def get_id(self):
           return (self.user_id)