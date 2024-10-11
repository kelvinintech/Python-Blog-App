import sqlite3
from flask import Flask, render_template, request

# Create the app instance
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    );
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()  # Fetch all posts
    conn.close()
    return render_template('index.html', posts=posts)  # Pass posts to the template

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']

    conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    conn.close()

    return render_template('index.html')  # Redirect to the homepage after adding the post

if __name__ == '__main__':
    create_table()  # Ensure the table is created when the app starts
    app.run(debug=True)
