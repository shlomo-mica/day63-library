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
#############################################################################################
# SQLITE3    connect with check_same_thread set to False.
db22 = sqlite3.connect("books_rate.db", check_same_thread=False)
cursor = db22.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS books("
    " title varchar(250) NOT NULL UNIQUE, "
    "author varchar(250) "
    "NOT NULL, rating FLOATNOT NULL)")
cursor.execute("INSERT OR IGNORE INTO books VALUES('Harry Potter', 'J. K. Rowling', '99')")
db22.commit()

all_books = []


def getAllRows():
    global connection, row
    try:
        connection = sqlite3.connect('books_rate.db')
        cursor_2 = connection.cursor()

        # print("Connected to SQLite")
        # ROWID = """SELECT rowid * from books"""
        sqlite_select_query = """SELECT * from books"""
        cursor_2.execute(sqlite_select_query)
        records = cursor_2.fetchall()

        # print("Total rows are:  ", len(records))
        # print("Printing each row")
        # for row in records:
        #
        #     print("Id: ", row[0])
        #     print("Name: ", row[1])
        #     print("Email: ", row[2])
        #     # print("Salary: ", row[3])
        #     print("\n")
        # print("records--", records[3])

        cursor_2.close()
        return records
    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            print("The Sqlite connection is closed")


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        book_author = request.form.get('book_author')
        book_score = request.form.get('book_score')
        # print(book_name, book_author, book_score)

        new_book_rating = {'book_name_title': book_name,
                           'author': book_author,
                           'book_score': book_score}
        all_books.append(new_book_rating)

        cursor.execute(f"INSERT OR REPLACE INTO books VALUES('{book_name}','{book_author}', '{book_score}')")
        db22.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/')
def home():
    getAllRows()
    # print("all books", all_books, getAllRows())
    var = getAllRows()
    return render_template('index.html', var=var)


list_rate = []


@app.route("/hello", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        new_rate_value = request.form.get('select')
        list_rate.append(new_rate_value)
        print(f"hello function value==", new_rate_value)
        return new_rate_value


@app.route('/rate/<b_name>-<int:c_name>', methods=['GET', 'POST'])
def rate(b_name, c_name):
    print(f"book name is={b_name, request.form.get('select')}")
    print("new value is=", c_name)
    new_rate_value = request.form.get('select')
    if c_name > 5:
        sql_update_query = f"""Update books SET rating =
                           '{new_rate_value}' WHERE title = 
                           '{b_name}' """
        cursor.execute(sql_update_query)
        db22.commit()
        print("the selecting rate is", new_rate_value)
    else:
        print("rate to low try again")

        return redirect(url_for('home'))
    return render_template("new_page_rate.html", name=request.form.get('select'), b_name=b_name)


@app.route('/delete/<b_name>')
def delete_book(b_name):
    # dee = input("what name to delete??")
    connnt = sqlite3.connect('books_rate.db')
    cursor = connnt.cursor()
    sql_update_query = """DELETE from books WHERE title = ?"""
    cursor.execute(sql_update_query, (b_name,))
    redirect(url_for("home"))
    connnt.commit()
    return redirect(url_for('home'))



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

# add_new_book = [book_name, book_author, book_score]
# db.session.add(add_new_book)
# db.commit()


# cursor.execute(f"INSERT OR REPLACE INTO books ({id == 2}) VALUES ('{name77}')")
# INSERT INTO phonebook(name,phonenumber) VALUES('Alice','704-555-1212')
#  ON CONFLICT(name) DO UPDATE SET phonenumber=excluded.phonenumber;
