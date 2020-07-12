import json
import os
import requests

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

main = Blueprint('main', __name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@main.route("/")
def index():
    return render_template('index.html')


@main.route("/home")
@login_required
def home():
    book = ""
    return render_template('home.html', name=current_user.name, book=book)


@main.route("/home", methods=['POST'])
@login_required
def home_post():
    isbn = '%' + request.form.get('isbn') + '%'
    title = '%' + request.form.get('title') + '%'
    author = '%' + request.form.get('author') + '%'
    books = []
    if isbn is not None:
        q1 = db.execute("SELECT title FROM bookinfo WHERE isbn LIKE (:isbn)", {"isbn": isbn}).fetchall()
        if len(q1) < 4999:
            books.append(q1)
    if title is not None:
        q2 = db.execute("SELECT title FROM bookinfo WHERE title LIKE (:title)", {"title": title}).fetchall()
        if len(q2) < 4999:
            books.append(q2)
    if author is not None:
        q3 = db.execute("SELECT title FROM bookinfo WHERE author LIKE (:author)", {"author": author}).fetchall()
        if len(q3) < 4999:
            books.append(q3)
    if not books:
        flash('No book found with given info')
    else:
        return render_template('home.html', book=books)
    return redirect(url_for('main.home', name=current_user.name))


@main.route("/bookpage")
def bookpage():
    data = []
    review_data = []
    return render_template('bookpage.html', data=data, review=review_data)


@main.route("/bookpage", methods=['POST'])
def bookpage_post():
    title = request.form.get('title')
    data = []
    i_data = []
    review_data = []
    rating = request.form.get('rating')
    reviews = request.form.get('review')
    bk_title = request.form.get('bk_title')
    if request.method == 'POST':
        if request.form.get('submit') == 'Get Details':
            if title is not None:
                q1 = db.execute("SELECT isbn, title, author, year FROM bookinfo WHERE title = (:title)",
                                {"title": title}).fetchall()
                q2 = db.execute("SELECT rating, review FROM reviews WHERE title = (:title)",
                                {"title": title}).fetchall()
                res = requests.get("https://www.goodreads.com/book/review_counts.json",
                                   params={"key": "13gygyrFyqYN9rxoJujKFw", "isbns": q1[0][0]})
                data.append(q1)
                if res.status_code == 422:
                    i_data.append("No data found! Please try again.")
                    i_data.append("No data found! Please try again.")
                else:
                    i_data.append(res.json()["books"][0]["work_ratings_count"])
                    i_data.append(res.json()["books"][0]["average_rating"])
                flash(res.json())
                if q2 is not None:
                    review_data.append(q2)
                    if len(review_data[0]) == 0:
                        review_data.clear()
                        review_data.append([('No Rating', 'No Reviews')])
        if request.form.get('submit') == 'Submit Review':
            q3 = db.execute("SELECT title FROM reviews WHERE title = (:title)",
                            {"title": bk_title}).fetchall()
            if len(q3) != 0:
                flash("Review already added")
            else:
                db.execute("INSERT INTO reviews (title, rating, review) VALUES (:title, :rating, :review)",
                           {"title": bk_title, "rating": rating, "review": reviews})
                db.commit()
    return render_template('bookpage.html', data=data, i_data=i_data, review=review_data, rating=rating,
                           reviews=reviews)


@main.route("/api/<isbn>", methods=['GET'])
def api(isbn):
    q1 = [[('1', 'n', 'n', 0)]]
    if 0 < len(isbn) <= 10:
        q1 = db.execute("SELECT title, author, year FROM bookinfo WHERE isbn = (:isbn)",
                        {"isbn": isbn}).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "13gygyrFyqYN9rxoJujKFw", "isbns": isbn})
    # avg_scr = res.json()['books'][0]['average_rating']
    # rev_c = res.json()['books'][0]['work_reviews_count']
    data = {"isbn": str(isbn), "title": q1[0][0][1], "author": q1[0][0][2], "year": q1[0][0][3],
            }
    return json.dumps(data)
