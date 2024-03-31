from flask import Flask, render_template, request, redirect

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
    cur.execute(
        'DROP TABLE soldiers'
    )
    cur.execute("""
        
        CREATE TABLE IF NOT EXISTS Soldiers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            army TEXT NOT NULL,
            unit TEXT NOT NULL
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
        army = request.form['army']
        unit = request.form['unit']

        conn = get_db_connection()

        # Check if email already exists
        cursor = conn.execute('SELECT id FROM Soldiers WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Email already exists, handle accordingly (e.g., show error message)
            conn.close()
            message = f"User with Email: {email} already exists!"
            return render_template('index.html', message=message)
        elif int(age) <= 18:
            conn.close()
            message = "Age must be greater than 18!"
            return render_template('index.html', message=message)
        elif army == "":
            conn.close()
            message = "Please make a selection for Army Status"
            return render_template('index.html', message=message)
        else:
            # Email does not exist, proceed to add user
            conn.execute('INSERT INTO Soldiers (name, lastname, email, age, army, unit) VALUES (?, ?, ?, ?, ?,?)',
                         (name, lastname, email, age, army, unit))
            conn.commit()
            # Check if email already exists
            cursor = conn.execute('SELECT name FROM Soldiers WHERE email = ?', (email,))
            user = cursor.fetchone()

            cursor = conn.execute('SELECT id FROM Soldiers WHERE email = ?', (email,))
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
        cursor = conn.execute('SELECT * FROM Soldiers WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if user:
            conn.execute('DELETE FROM Soldiers WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            message2 = f"User with ID: {user_id} deleted successfully!"
            return render_template('index.html', message2=message2, user_id=user_id)
        else:
            conn.close()
            message2 = f"No user found with ID: {user_id}."
            return render_template('index.html', message2=message2, user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)
