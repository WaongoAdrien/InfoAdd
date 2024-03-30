from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# Function to create a connection to SQLite database
def get_db_connection():
    conn = sqlite3.connect('user_info.db')
    conn.row_factory = sqlite3.Row
    return conn


# Create table if not exists
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS family (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL
        );
    """)
    conn.commit()
    conn.close()


create_table()


# Route to show the form for adding a new user
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        age = request.form['age']

        conn = get_db_connection()

        # Check if email already exists
        cursor = conn.execute('SELECT id FROM family WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Email already exists, handle accordingly (e.g., show error message)
            conn.close()
            message = f"User with Email: {email} already exists!"
            return render_template('index.html', message=message)
        else:
            # Email does not exist, proceed to add user
            conn.execute('INSERT INTO family (name, lastname, email, age) VALUES (?, ?, ?, ?)',
                         (name, lastname, email, age))
            conn.commit()
            # Check if email already exists
            cursor = conn.execute('SELECT name FROM family WHERE email = ?', (email,))
            user = cursor.fetchone()

            cursor = conn.execute('SELECT id FROM family WHERE email = ?', (email,))
            user_id = cursor.fetchone()

            conn.close()
            # Access the name attribute of the user object
            name = user['name']
            user_id = user_id['id']
            message = f"Congratulations {name} added successfully! Id : {user_id}"
            return render_template('index.html', message=message)


@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        user_id = request.form['id']
        conn = get_db_connection()
        cursor = conn.execute('SELECT * FROM family WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if user:
            conn.execute('DELETE FROM family WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            message2 = f"User with ID: {user_id} deleted successfully!"
            return render_template('index.html', message2=message2, user_id=user_id)
        else:
            conn.close()
            message2 = f"No user found with ID: {user_id}."
            return render_template('index.html', message2=message2, user_id=user_id)


