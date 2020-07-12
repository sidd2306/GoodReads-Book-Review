import os, csv

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:  # loop gives each column a name
        db.execute("INSERT INTO bookinfo (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author,
                    "year": year})  # substitute values from CSV line into SQL command, as per this dict
        print(f"Added {isbn},{title} ,{author} ,{year} ")
    db.commit()  # transactions are assumed, so close the transaction finished


if __name__ == "__main__":
    main()
