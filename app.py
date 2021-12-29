# "Flask Run" to start development server locally. 

from flask import Flask, render_template, Markup
import sqlite3 
from markupsafe import escape


app = Flask(__name__)

def get_db_connection(): 
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_posts():
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return posts

@app.route("/")
def index():
    posts = get_posts()
    """
    x = 0
    print(posts)
    for temp_post in posts: 
        temp_post = dict(temp_post)
        for key, value in temp_post.items(): 
            new_value = Markup(value).unescape()
            temp_post[key] = new_value
        print(temp_post)
        posts[x] = temp_post
        x += 1
    print(posts)
    """
    return render_template('index.html', posts=posts)

@app.route("/posts/<i>")
def show_post(i):
    i = escape(i)
    try: 
        i = int(i)
        posts = get_posts()
        # print(posts)
        post = dict(posts[i])
        for key, value in post.items(): 
            new_value = Markup(value).unescape()
            post[key] = new_value
        return render_template("page.html", post = post)
    except ValueError: 
        return render_template("404.html")

@app.route("/<slug>")
def show_post_slug(slug):
    slug = escape(slug)
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    post_number = connection.execute(f"SELECT * FROM posts WHERE slug='{slug}';").fetchone()
    try: 
        post = dict(post_number)
        # print(post)
        for key, value in post.items(): 
            new_value = Markup(value).unescape()
            post[key] = new_value
        # print(post)

        return render_template("page.html", post=post)
    except TypeError: 
        return render_template("404.html")