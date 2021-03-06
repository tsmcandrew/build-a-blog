from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blog_title = db.Column(db.String(120))
    blog_body = db.Column(db.String(500))
    blog_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    

    def __init__(self, blog_title, blog_body):
       
        self.blog_title = blog_title 
        self.blog_body = blog_body 
        


"""class NewBlog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.pw_hash = make_pw_hash(password)"""


"""@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'static']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')"""


"""@app.route('/blog.html', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_pw_hash(password, user.pw_hash):
            session['email'] = email
            flash("Logged in", 'info')
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'danger')

    return render_template('login.html')"""


"""@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #verify = request.form['verify']

        # todo - validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            flash("The email <strong>{0}</strong> is already registered".format(email), 'danger')

    return render_template('register.html')"""

"""@app.route('/logout', methods=['POST'])
def logout():
    del session['email']
    return redirect('/')"""


@app.route('/blog', methods=['POST', 'GET'])
def index():

    blog_id = request.args.get('id')
    

    if request.args.get('id') is not None: 
        
        blog = Blog.query.get(blog_id)  
        blog_title = blog.blog_title
        blog_body = blog.blog_body
        
        return render_template('id_blog.html', 
            blog_body=blog_body, blog_title=blog_title, blog_id=blog_id)
    
    else: 
        existing_blogs = Blog.query.order_by(Blog.blog_date.desc()).all()
        
        return render_template('blog.html', 
            existing_blogs=existing_blogs)
    


@app.route('/newpost', methods=['GET', 'POST'])
def newpost(): 
    
    if request.method == 'POST':
        
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        # blog_date = request.form['blog_date']
        newpost = Blog(blog_title, blog_body) 
        # , blog_date)
        db.session.add(newpost)
        db.session.commit()
        db.session.flush()
        blog_id = newpost.id
        
        
        # add code to test if blog entry, body & title, are empty. Return error message and newpost form.

        if blog_title == '' or blog_body == '': 
            
            title_error = 'Oops! You forgot to input a Title for your piece.'
            body_error = 'Oops! You forgot to jot down your next masterpiece.'

            return render_template('newpost.html', blog_title=blog_title, blog_body=blog_body, 
                title_error=title_error, body_error=body_error)

        else: 
            
            blog_id = newpost.id
            return redirect('/blog?id={0}'.format(blog_id))

    else: 
            
        return render_template('newpost.html')


if __name__ == '__main__':
    app.run()
