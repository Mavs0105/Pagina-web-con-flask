from flask import Flask, render_template, request, redirect, session, url_for
import bcrypt
import os
import json

app = Flask(__name__)

db_file_path = os.path.join(os.path.dirname(__file__), 'Users.json')

def load_users():
    with open(db_file_path, 'r') as f:
        return json.load(f)

def save_users(Users):
    with open(db_file_path, 'w') as f:
        json.dump(Users, f, indent=4)


def user_exists(email):
    Users = load_users()
    for User in Users['Users']:
        if User['email'] == email:
            return True
    return False

@app.route('/')
def index():
    return redirect(url_for('Login'))

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        Users = load_users()
        for User in Users['Users']:
            if User['email'] == email and bcrypt.checkpw(password, User['password'].encode('utf-8')):
                session['User']=email
                return redirect(url_for('Home'))
        return '😵 Credenciales incorrectas, intente de nuevo'
    return render_template('Login.html')

@app.route('/Register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        if user_exists(email):
            return '🙄 El usuario ya existe. Por favor, inicia sesión.'
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        new_user = {'email': email, 'password': hashed_password.decode('utf-8')}
        Users = load_users()
        Users['Users'].append(new_user)
        save_users(Users)
        return redirect(url_for('Login'))
    return render_template('Register.html')



@app.route('/Home')
def Home():
    return render_template('Home.html')


@app.route('/Customers')
def Customers():
    return render_template('Customers.html')


@app.route('/Users')
def Users():
    return render_template('Users.html')

@app.route('/Profile')
def Profile():
    if 'User' in session:
        User_email = session['User']
        return render_template('Profile.html', User=User_email)
    return redirect(url_for('Login'))

@app.route('/Logout')
def Logout():
    session.pop('User', None)
    return redirect(url_for('Login'))


if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.run(debug=True)
