from flask import Flask, render_template, request, session, make_response, redirect
from init import *

from backend.functions import verify_password

import threading

app = Flask(__name__, static_url_path=static_url_path, static_folder=static_folder, template_folder=template_folder)

app.config['SECRET_KEY'] = secret

def logged_in(session):
    try:
        db = sql.connect('backend/data.db')
        c = db.cursor()
        c.execute('SELECT * FROM users WHERE account_username = ? AND password = ?', (session.get("_strawberryid.username"), session.get("_strawberryid.password")))
        logged_in=c.fetchall()

    except Exception as e:
        logged_in=False

    if logged_in:
        return True
    else:
        return False

# request_counter = 0
# @app.before_request
# def count_requests():
#     global request_counter
#     request_counter += 1
    
# # Route, um die Anzahl der Anfragen anzuzeigen
# @app.route('/requests')
# def show_requests():
#     return f'Anzahl der Anfragen: {request_counter}'

@app.route("/", defaults={'lang': 'en'})
@app.route('/<string:lang>')
def index(lang):
    is_authenticated = False
    
    if logged_in(session):
        username = session.get("_strawberryid.username")
        profile_picture_url = session.get("_strawberryid.avatarurl")
        name = session.get("_strawberryid.name")
        is_authenticated = True
    else:
        username, profile_picture_url, name = None, None, None
    
    def StringLoader(str):
        return strloader(lang, str)
        
    return render_template('index.html', loader=StringLoader, lang=lang, is_authenticated=is_authenticated, username=username, profile_picture_url=profile_picture_url, account_name=name)

# Login
@app.route("/login", defaults={'lang': 'en'}, methods=['GET', 'POST'])
@app.route('/<string:lang>/login', methods=['GET', 'POST'])
def login(lang):
    error = False
        
    def StringLoader(str):
        return strloader(lang, str)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"A login received: {username}:{password}")
        db = sql.connect('backend/data.db')
        c = db.cursor()
        
        c.execute("SELECT password FROM users WHERE account_username = ?", (username,))
        result = c.fetchone()
        
        if result is not None:
            stored_password = result[0]
            
            if verify_password(stored_password, password):
                c.execute('SELECT account_username, password, profile_picture_url, name FROM users WHERE account_username = ?', (username,))
                result = c.fetchone()
                
                # If username exists, login the user
                if result is not None:
                    username            = result[0]
                    password            = result[1]
                    profile_picture_url = result[2]
                    name                = result[3]
                    
                    session["_strawberryid.username"] = username
                    session["_strawberryid.password"] = password
                    session["_strawberryid.avatarurl"] = profile_picture_url
                    session["_strawberryid.name"] = name
                    
                    print("Login successful")
            else:
                error = True
                print("Error while verifing password!")
        else:
            error = True
            print("Invalid username and/or password!")
        
    return render_template('login.html', loader=StringLoader, lang=lang, error=error, redirect=redirect)

# Logout
@app.route("/logout", defaults={'lang': 'en'}, methods=['GET', 'POST'])
@app.route('/<string:lang>/logout', methods=['GET', 'POST'])
async def logout(lang):
    session.pop('_strawberryid.username', None)
    session.pop('_strawberryid.password', None)
    session.pop('_strawberryid.avatarurl', None)
    session.pop('_strawberryid.name', None)

    return redirect(f"/{lang}")


@app.route("/account", defaults={'lang': 'en'})
@app.route('/<string:lang>/account')
def account(lang):
    is_authenticated = False
    if not logged_in(session):
        print("You must be logged in")
        return redirect(f"/{lang}/login")


    if logged_in(session):
        username = session.get("_strawberryid.username")
        profile_picture_url = session.get("_strawberryid.avatarurl")
        name = session.get("_strawberryid.name")
        is_authenticated = True
    else:
        username, profile_picture_url, name = None, None, None
    
    def StringLoader(str):
        return strloader(lang, str)
        
    return render_template('account.html', loader=StringLoader, lang=lang, is_authenticated=is_authenticated, username=username, profile_picture_url=profile_picture_url, account_name=name)



if __name__ == "__main__":
    app.run(host=ip_address, port=port, debug=debug_mode, threaded=threaded)