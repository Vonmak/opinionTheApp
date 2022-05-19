from flask import render_template, request, abort, url_for, redirect, flash
from . import main
from ..models import Blog, User, Comment, Subscriber
from .forms import UpdateProfile, BlogForm, CommentForm
from .. import db, photos
from flask_login import login_required, current_user
from app.requests import get_quotes
from ..email import mail_message


@main.route('/', methods = ['GET','POST'])
# @login_required
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - The Best Blog Website'
    blogs = Blog.query.filter_by().first()
    quotes = get_quotes()
    return render_template('index.html',title = title, blogs=blogs, quote=quotes)


@main.route('/comments')
# @login_required
def view():
    posts = Blog.query.all()
    
    return render_template('comments.html', posts=posts)

@main.route('/blogs/new/', methods = ['GET','POST'])
# @login_required
def new_blog():
    form = BlogForm()
   
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        
        new_blog = Blog(user_id=current_user.id, title = title,description=description)
        new_blog.save_blog()
        
        
        return redirect(url_for('main.index'))
    return render_template('new_blog.html',form=form)

@main.route('/blog/<id>')
def blog(id):
    comments = Comment.query.filter_by(blog_id=id).all()
    blog = Blog.query.get(id)
    return render_template('blog.html',blog=blog,comments=comments)
    
@main.route('/blog/<blog_id>/delete', methods = ['POST'])
# @login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("You have deleted your Blog successfully!")
    return redirect(url_for('main.index'))



@main.route('/comment/<blog_id>', methods = ['Post','GET'])
# @login_required
def new_comment(blog_id):
    blog = Blog.query.get(blog_id)
    comment =request.form.get('newcomment')
    new_comment = Comment(comment = comment, blog_id=blog_id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('main.blog',id = blog.id))


@main.route('/comment/<blog_id>/delete', methods = ['POST'])
def delete_comment(blog_id):
    comment = Comment.query.get(blog_id)
    if comment.user != current_user:
        abort(403)
    comment.delete()
    flash("You have deleted your Comment successfully!")
    return redirect(url_for('main.index'))

@main.route('/profile/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/profile/<uname>/update',methods = ['GET','POST'])
# @login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    
    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic', methods=['POST'])
# @login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))


@main.route('/user/<username>')
def posts(username):
    
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page',1, type = int )
    # blogs= Blog.get_blog(blog_id)
    blogs = Blog.query.filter_by(user=user).order_by(Blog.date_posted.desc()).paginate(page = page, per_page = 4)
    return render_template('user.html',blogs=blogs,user = user)
 


@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to Blog Play","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Successfully subscribed')
    return redirect(url_for('main.index'))