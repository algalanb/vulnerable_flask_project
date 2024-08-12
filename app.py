from flask import Flask, request, render_template, redirect, url_for, session, g, flash
from db.database import connect_db, add_user
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def index():
    if 'username' in session:
        return f"Welcome {session['username']}!"
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = g.db
        cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            flash('El nombre de usuario ya existe. Por favor, elige otro.', 'error')
            return redirect(url_for('register'))
        else:
            add_user(username, password)
            flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = g.db
        cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("Nombre de usuario o contraseña incorrectos. Inténtalo de nuevo.", 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
