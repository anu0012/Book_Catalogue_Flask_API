from flask import Blueprint, g, current_app, Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from config import BaseConfig
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse

from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from forms import LoginForm
from forms import RegistrationForm
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from book_api import get_book_details

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Book(UserMixin, db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(128))
    username = db.Column(db.String(64), index=True)
    title = db.Column(db.String(128))
    authors = db.Column(db.String(128))
    pageCount = db.Column(db.Integer)
    rating = db.Column(db.String(128))

    def __repr__(self):
        return '<Book {}>'.format(self.username)


@app.route('/')
def index():
    if current_user.is_authenticated:
        books = Book.query.filter_by(username=current_user.username).all()
        return render_template("index.html", title='Home Page', books=books)
    return render_template("index.html", title='Home Page')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            error = 'Invalid username or password'
            return render_template('login.html', form=form, error=error)

        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data.strip())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return 'Username is already taken. Please try another one!!!'

    return render_template('register.html', title='Register', form=form)


@app.route('/search/', methods=['POST'])
@login_required
def search():
    isbn = request.form['bookISBN']
    output = get_book_details(isbn.strip())
    if len(output) > 0:
        # store in DB if ISBN is not there for the current user
        if Book.query.filter_by(username=current_user.username).filter_by(isbn=isbn.strip()).count() == 0:
            book = Book(isbn=isbn.strip(), username=current_user.username, title=output['title'],
            authors=output['authors'], pageCount=output['pageCount'], rating=output['maturityRating'])
            db.session.add(book)
            db.session.commit()
        else:
            return 'ISBN is already in the record. Please try another one!!!'
    else:
        "Invalid ISBN. Please try again!!!"
    return redirect(url_for('index'))


@app.route('/delete/<book_id>', methods=['GET'])
@login_required
def delete(book_id):
    Book.query.filter_by(username=current_user.username).filter_by(isbn=book_id.strip()).delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)