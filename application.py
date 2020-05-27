import os, requests

from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#registration page
@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html", log_message="Log in")

# Register route - triggered when user fills in Registration form; routes to log in
@app.route("/register", methods=["POST"])
def register():
    # Get form information.
    first_name = request.form.get("first_name")
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if user exists
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount != 0:
        return render_template("error.html", message="You already have an account. Go back to log in.", log_message="Log in")
    
    # Add user to database.
    db.execute("INSERT INTO users (first_name, username, password) VALUES (:first_name, :username, :password)",
            {"first_name": first_name, "username": username, "password": password})
    db.commit()
    return redirect(url_for('login'))

#log in page
@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html", log_message="Log in")

# log in route - triggered when user enters info on log in page, goes to home
@app.route("/logging_in", methods=["POST"])
def logging_in():
    # Get form information.
    username = request.form.get("username")
    password = request.form.get("password")

    #Check if user exists
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password" : password}).rowcount == 0:
        return render_template("error.html", message="This username or password is wrong.", log_message="Log in") 
    
    # log user in
    user = db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password" : password}).fetchone()
    session["user_id"] = user.user_id #saves session
    db.commit()
    return redirect(url_for('home'))

#log out
@app.route("/logout", methods=["POST"])
def logout():
    if "user_id" in session:
        session.pop("user_id")
    return redirect(url_for('login'))

#home page when user logs in
@app.route("/home", methods=["POST", "GET"])
def home():
    
    if "user_id" not in session:
        return redirect(url_for('login'))

    user = db.execute("SELECT * FROM users WHERE user_id = :user_id", {"user_id": session["user_id"]}).fetchone()
    db.commit()
    return render_template("home.html", log_message="Log out", user=user)

#search
@app.route("/search", methods=["POST"])
def search():
    if "user_id" not in session:
        return redirect(url_for('login'))
    
    #get form info
    placeholder = request.form.get("search-keyword")
    keyword = f'%{placeholder}%' #makes it so you can search just a part of the keyword
    
    book_list = []
    book_list = db.execute("SELECT * FROM books WHERE (isbn ILIKE :keyword) OR (title ILIKE :keyword) OR (author ILIKE :keyword)", {"keyword": keyword}).fetchall()
    if len(book_list) == 0: #if there are no matching books ******* make into banner later?
        return render_template("error.html", message="No books found.")
    #lists all books that match 
    db.commit()
    return render_template("books.html", book_list=book_list, log_message="Log out")

#individual book page
@app.route("/book/<isbn>", methods=["GET", "POST"])
def book(isbn):
    if "user_id" not in session:
        return redirect(url_for('login'))
    
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone() #gets the title from the database
    
    #Goodreads API
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "QikazWK11kUJNnHXepN9Iw", "isbns": isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    
    book_object = res.json() #turns it into JSON
    book_result = book_object['books'][0]

    #gets the number of ratings & avg rating from Goodreads, which will be displayed
    number_ratings = book_result['work_ratings_count'] 
    avg_rating = book_result["average_rating"]

    #Reviews 
    already_reviewed = False
    
    if request.method == "POST":
        review = request.form.get("review")
        rating = request.form.get("rating")
        date = datetime.date(datetime.now())

        #post review
        if already_reviewed == False:
            db.execute("INSERT INTO reviews (isbn, review, user_id, rating, date) VALUES (:isbn, :review, :user_id, :rating, :date)", {"isbn": isbn, "review": review, "user_id": session["user_id"], "rating": int(rating), "date": date})
    
    #check if already reviewed
    if db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND isbn = :isbn", {"user_id": session["user_id"], "isbn": isbn}).rowcount > 0:
        already_reviewed = True
    
    #print reviews
    reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    # TODO: talk about join 
    user = db.execute("SELECT * FROM users JOIN reviews ON users.user_id = reviews.user_id WHERE isbn = :isbn", {"isbn": isbn}).fetchall() 
    
    # get stats
    bookclub_avg_rating = False
    bookclub_number_ratings = False
    if db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).rowcount>0: 
        bookclub_avg_rating = db.execute("SELECT ROUND(AVG(rating), 2) FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchone()[0]
        bookclub_number_ratings = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).rowcount
        print(bookclub_number_ratings)
    db.commit()
    return render_template("book.html", book=book, number_ratings=number_ratings, avg_rating=avg_rating, reviews=reviews, isbn=isbn, already_reviewed=already_reviewed, user=user, log_message="Log out", bookclub_avg_rating=bookclub_avg_rating, bookclub_number_ratings=bookclub_number_ratings)

# Shows all books user has reviewed
@app.route("/your_books", methods=["GET", "POST"])
def your_books():
    if "user_id" not in session:
        return redirect(url_for('login'))

    #pull list of all the books user has reviewed
    your_books = db.execute("SELECT * FROM reviews JOIN books ON reviews.isbn = books.isbn WHERE reviews.user_id = :user_id", {"user_id": session["user_id"]}).fetchall()
    db.commit()
    return render_template("your_books.html", your_books=your_books, log_message="Log out")


#API
@app.route("/api/books/<isbn>")
def book_api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid ISBN"}), 422

    bookclub_avg_rating = bookclub_avg_rating = db.execute("SELECT ROUND(AVG(rating), 2) FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchone()[0]
    bookclub_number_ratings = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).rowcount
    db.commiy()

    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": bookclub_number_ratings,
        "average_score": bookclub_avg_rating
    })
    

