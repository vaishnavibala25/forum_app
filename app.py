from flask import Flask, render_template, request, redirect, url_for, flash, session
from mongoengine import connect
from models.post_model import Post
from models.reply_model import Reply
from models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(_name_)
app.secret_key = 'your_secret_key'
# Connect to MongoDB using MongoEngine
connect('forum_database', host='localhost', port=27017)
@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.objects(username=username).first():
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        user.save()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.objects(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            flash('Login successful!', 'success')  # Flash a success message
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'error')  # Flash an error message
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = User.objects(username=session['username']).first()
    if request.method == 'POST':
        email = request.form['email']
        bio = request.form['bio']
        
        # Update the user's details in the database
        user.update(email=email, bio=bio)

        flash('Profile updated successfully!')
        return redirect(url_for('profile'))  # Redirect to the profile page to reflect the changes

    return render_template('update_profile.html', user=user)


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    posts = Post.objects()  # Retrieve all posts
    return render_template('dashboard.html', posts=posts)

@app.route('/create_post', methods=['POST'])
def create_post():
    title = request.form.get('title')
    content = request.form.get('content')
    new_post = Post(title=title, content=content)
    new_post.save()
    return redirect(url_for('dashboard'))

@app.route('/like/<post_id>', methods=['POST'])
def like_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    post = Post.objects.get(id=post_id)
    user_id = session['username']

    if user_id in post.likes:
        flash("You have already liked this post.", "error")
    else:
        post.update(push__likes=user_id)
        flash("Post liked successfully!", "success")

    return redirect(url_for('dashboard'))


@app.route('/reply/<post_id>', methods=['POST'])
def reply(post_id):
    content = request.form.get('content')
    post = Post.objects.get(id=post_id)  # Find the post to reply to
    new_reply = Reply(content=content, post=post)
    new_reply.save()
    post.update(push__replies=new_reply)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    return redirect(url_for('login'))


if _name_ == '_main_':
    app.run(debug=True)