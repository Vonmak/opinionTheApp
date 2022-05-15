from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    blogs = db.relationship('Blog', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref = 'user', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'
    
    
# class Blog(db.Model):
#     __tablename__ = 'blogs'

#     id = db.Column(db.Integer, primary_key = True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
#     description = db.Column(db.String(), index = True)
#     title = db.Column(db.String())
#     date_posted = db.Column(db.DateTime(250), default=datetime.utcnow)
#     comments = db.relationship('Comment',backref='blogs',lazy='dynamic') 
    
    
#     def save_blogs(self):
#         db.session.add(self)
#         db.session.commit()
        
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
    
#     @classmethod
#     def get_blogs(cls):
#         blogs = Blog.query.filter_by(blogs_id=id).all()
#         return blogs

#     def __repr__(self):
#         return f"blogs {self.title}"
    
   
    
    
     
# class Comment(db.Model):
    
#     __tablename__ = 'comments'

#     id = db.Column(db.Integer,primary_key=True)
#     comment= db.Column(db.String)
#     blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     date_posted = db.Column(db.DateTime(250), default=datetime.utcnow)
    

#     def save_comment(self):
#         '''
#         Function that saves comments
#         '''
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         db.session.remove(self)
#         db.session.commit()

#     def get_comments(cls):
#         comment = Comment.query.all(id=id)
#         return comment
    
#     def __repr__(self):
#         return f'Comment {self.comment}'
    
# class Subscriber(db.Model):
    # __tablename__='subscribers'

    # id=db.Column(db.Integer,primary_key=True)
    # email = db.Column(db.String(255),unique=True,index=True)

    # def save_subscriber(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def __repr__(self):
    #     return f'Subscriber {self.email}'