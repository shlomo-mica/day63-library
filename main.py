from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, session
import sqlite3

app = Flask(__name__)
##CREATE DATABASE

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books.db"

# Create the extension
db = SQLAlchemy()
# Initialise the app with the extension
db.init_app(app)


##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


# Optional: this will allow each book object to be identified by its title when printed.
def __repr__(self):
    return f'<Book {self.title}>'


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()

# CREATE RECORD SQLAlchemy!!
# with app.app_context():
#     new_book = Book(id=11, title="Harry Potter", author="J. K. Rowling", rating=9.3)
#     db.session.add(new_book)
#     db.session.commit()

# SQLITE3    connect with check_same_thread set to False.
db22 = sqlite3.connect("new-books.db", check_same_thread=False)
cursor = db22.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) "
    "NOT NULL, rating FLOATNOT NULL)")
cursor.execute("INSERT OR IGNORE INTO books VALUES('5', 'Harry Potter', 'J. K. Rowling', '99')")
db22.commit()

all_books = []


@app.route('/')
def home():
    test = 'TEST'
    return render_template('index.html', all_books=all_books, test=test)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        book_author = request.form.get('book_author')
        book_score = request.form.get('book_score')
        print(book_name, book_author, book_score)

        # add_new_book = [book_name, book_author, book_score]
        # db.session.add(add_new_book)
        # db.commit()

        new_book_rating = {'book_name_title': book_name,
                           'author': book_author,
                           'book_score': book_score}
        all_books.append(new_book_rating)

        cursor.execute(f"INSERT OR REPLACE INTO books VALUES('5','{book_name}','{book_author}', '{book_score}')")
        db22.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/rate', methods=['GET', 'POST'])
def hello(name77='GOOD DAY'):
    if request.method == 'POST':
        cursor.execute("UPDATE books SET rating = 55 WHERE id = 2")
        db22.commit()
        # cursor.execute(f"INSERT OR REPLACE INTO books ({id == 2}) VALUES ('{name77}')")
        print(request.form.get('select'))
        return redirect(url_for('home'))
    return render_template("new_page_rate.html", name=request.form.get('select'))


# INSERT INTO phonebook(name,phonenumber) VALUES('Alice','704-555-1212')
#  ON CONFLICT(name) DO UPDATE SET phonenumber=excluded.phonenumber;

if __name__ == "__main__":
    app.run(debug=True)

# new_book = Book(
#             title=request.form["title"],
#             author=request.form["author"],
#             rating=request.form["rating"]
#         )
#         db.session.add(new_book)
#         db.session.commit()
#         return redirect(url_for('home'))
#     return render_template("add.html"

# solution from Angela
# @app.route('/')
# def home():
#     ##READ ALL RECORDS
#     # Construct a query to select from the database. Returns the rows in the database
#     result = db.session.execute(db.select(Book).order_by(Book.title))
#     # Use .scalars() to get the elements rather than entire rows from the database
#     all_books = result.scalars()
#     return render_template("index.html", books=all_books)

# TODO# LIST OF DICTIONARY
# for item in all_books:
#     for i in item:
#         print(i)
