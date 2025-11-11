import os
import sqlite3
import joblib
import secrets
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
model = joblib.load('model/spam_model.pkl')
app.secret_key = 'supersecretkey'
from flask_mail import Mail, Message

# Configure your email (use Gmail or similar)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with your Gmail
app.config['MAIL_PASSWORD'] = 'trct joqb fyjf vqvj'     # Use App Password (not Gmail password)
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)


# 🔥 Force Flask to use the correct database file
DB_PATH = r"D:\cp-1\database.db"

def get_connection():
    print(f"Connecting to DB: {DB_PATH}")  # For debugging
    return sqlite3.connect(DB_PATH)

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DB_PATH = r"D:\cp-1\database.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    # This will show the **real file path** SQLite opened
    print("Connected database file:", conn.execute("PRAGMA database_list").fetchall())
    return conn


# --- Database setup ---
def init_db():
    conn = get_connection()
    print(f"Connecting to DB: {DB_PATH}")


    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'user'
                )''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            conn = get_connection()

            c = conn.cursor()
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            conn.close()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('index'))
        except:
            flash('Email already registered!', 'danger')
            return redirect(url_for('signup'))
    return render_template('signup.html')
    import secrets

reset_tokens = {}  # temporary in-memory token store

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()

        if user:
            token = secrets.token_urlsafe(16)
            reset_tokens[token] = email

            reset_link = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', recipients=[email])  # ✅ send to user email
            msg.body = f"""
Hi {user[1]},
We received a request to reset your password.
Click the link below to reset it:

{reset_link}

If you didn't request this, please ignore this email.
"""
            mail.send(msg)

            flash('Password reset link sent to your email!', 'info')
            return redirect(url_for('index'))
        else:
            flash('No account found with that email.', 'danger')
            return redirect(url_for('forgot_password'))

    return render_template('forgot-password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = reset_tokens.get(token)
    if not email:
        flash('Invalid or expired token!', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_password = request.form['password']
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
        conn.commit()
        conn.close()
        reset_tokens.pop(token)
        flash('Password updated successfully! You can now log in.', 'success')
        return redirect(url_for('index'))

    return render_template('reset-password.html', token=token)


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        session['user'] = user[1]
        session['role'] = user[4]
        if user[4] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    else:
        flash('Invalid email or password', 'danger')
        return redirect(url_for('index'))
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    email_text = request.form['email_text']
    prediction = model.predict([email_text])[0]

    return render_template('user-dashboard.html', name=session['user'], result=prediction)
    
@app.route('/user-dashboard')
def user_dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('user-dashboard.html', name=session['user'])

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE role='user'")
    total_users = c.fetchone()[0]
    conn.close()
    return render_template('admin-dashboard.html', name=session['user'], total_users=total_users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/debug-users')
def debug_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, email, password, role FROM users")
    users = c.fetchall()
    conn.close()
    return f"<pre>{users}</pre>"


if __name__ == '__main__':
    app.run(debug=True)
