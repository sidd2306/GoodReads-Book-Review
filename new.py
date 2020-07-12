import requests

res = requests.get("https://www.goodreads.com/book/review_counts.json",
                   params={"key": "13gygyrFyqYN9rxoJujKFw", "isbns": "1416523715"})
print(res.json()['books'][0]['average_rating'])
