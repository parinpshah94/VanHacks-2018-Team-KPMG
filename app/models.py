from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_points = db.Column(db.Numeric, default=0)
    about_me = db.Column(db.String(140))

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def nemo(self):
        return 'https://vignette.wikia.nocookie.net/pixar/images/8/82/Nemo.png'

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    def get_total_collect(self):
        all_posts_cursor = db.session.execute('select * from post where user_id=:id', {'id': self.id})
        all_points = []
        for post in all_posts_cursor:
            all_points.append(post[3])  # the 4th column is point
        return sum(all_points)

    def get_monthly_collect(self):
        group_by_statement = "SELECT strftime('%Y', timestamp) as valYear, strftime('%m', timestamp ) as valMonth, SUM(points) FROM post where user_id=:id GROUP BY valYear, valMonth"
        all_posts_cursor = db.session.execute(group_by_statement, {'id': self.id})
        monthly_posts = []
        for post in all_posts_cursor:
            monthly_posts.append({str(post[0]) + '-' + str(post[1]): post[2]})  # the 4th column is point
        return monthly_posts

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    points = db.Column(db.Numeric, default=0)
    items = db.Column(db.String(140))
    img_id = db.Column(db.String(140))
    body = db.Column(db.String(140))
    language = db.Column(db.String(5))
    soft_plastic = db.Column(db.Numeric, default=0)
    hard_plastic = db.Column(db.Numeric, default=0)
    styrofoam = db.Column(db.Numeric, default=0)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    def calculate_points(self):
        dimension_dict = {
            'soft_plastic': 2,
            'hard_plastic': 3,
            'styrofoam': 4
        }

        self.points = (dimension_dict['soft_plastic'] * self.soft_plastic) + (dimension_dict['hard_plastic'] * self.hard_plastic) + (dimension_dict['styrofoam'] * self.styrofoam)

    def generate_body(self):
        self.body = 'I earned ' + str(self.points) + ' points by recycling '
        word_list = []
        if self.hard_plastic:
            word_list.append(str(self.hard_plastic) + ' grams of hard plastic')
        if self.soft_plastic:
            word_list.append(str(self.soft_plastic) + ' grams of soft plastic')
        if self.styrofoam:
            word_list.append(str(self.styrofoam) + ' grams of styrofoam')
        self.body += ', '.join(word_list) + '.'



class Redeem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    points = db.Column(db.Numeric)
    reward = db.Column(db.String(140))
    partner = db.Column(db.String(140))