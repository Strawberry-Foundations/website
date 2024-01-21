from flask import Flask, render_template, request, session, make_response, redirect, jsonify
from init import *

from backend.functions import verify_password

import requests
from urllib.parse import quote

app = Flask(__name__, static_url_path=static_url_path, static_folder=static_folder, template_folder=template_folder)

app.config['SECRET_KEY'] = secret

def logged_in(session):
    try:
        db = sql.connect('backend/data.db')
        c = db.cursor()
        # c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (session.get("_strawberryid.username"), session.get("_strawberryid.password")))
        c.execute('SELECT * FROM users WHERE username = ?', (session.get("_strawberryid.username"),))
        logged_in=c.fetchall()

    except Exception as e:
        logged_in=False

    if logged_in:
        return True
    else:
        return False

# IMPORTANT: Query parameters need to look like ?v=desktop&code=123456
# Index page
@app.route("/", defaults={'lang': 'en'})
@app.route('/<string:lang>')
def index(lang):
    def StringLoader(str):
        return strloader(lang, str)     
    
    is_authenticated = False
    view_type = request.args.get('v', default=False)
    code = request.args.get('code', default='none')
    
    if not view_type:
        return js_screen_size_script
    
    if logged_in(session):
        db = sql.connect('backend/data.db')
        c = db.cursor()
        
        username = session.get("_strawberryid.username")
        profile_picture_url = session.get("_strawberryid.avatarurl")
        name = session.get("_strawberryid.full_name")
        is_authenticated = True
        
        # c.execute('SELECT cloud_engine_enabled FROM users WHERE username = ? AND password = ?', (session.get("_strawberryid.username"), session.get("_strawberryid.password")))
        c.execute('SELECT cloud_engine_enabled FROM users WHERE username = ?', (session.get("_strawberryid.username"),))
        result = c.fetchall()
        allowed_ce = result[0]
        
    else:
        username, profile_picture_url, name, allowed_ce = None, None, None, "false"
      
    return render_template('index.html',
                           loader=StringLoader,
                           lang=lang,
                           is_authenticated=is_authenticated,
                           username=username,
                           profile_picture_url=profile_picture_url,
                           account_name=name,
                           view_type=view_type,
                           allowed_ce=allowed_ce[0])


@app.route("/login", defaults={'lang': 'en'}, methods=['GET', 'POST'])
@app.route('/<string:lang>/login', methods=['GET', 'POST'])
def login(lang):
    login_type = request.args.get('lt', default="global")

    if login_type == "local":
        return redirect(f"{strawberry_id_domain}{lang}?redirect=http://{request.url_root.replace('http://', '').replace('https://', '').replace('/', '')}&hl={lang}")
    else: 
        return redirect(f"{strawberry_id_domain}{lang}?redirect=https://strawberryfoundations.xyz&hl={lang}")


@app.route("/callback", methods=['GET', 'POST'])
def callback():
    redir_lang = request.args.get('hl', default="en")
    
    if not "code" in request.args:
        return redirect("/" + redir_lang)
    
    data = requests.get(strawberry_id_domain + "validate?code=" + quote(request.args["code"])).json()["data"]
    session["_strawberryid.username"]   = data["username"]
    # session["_strawberryid.password"]   = password
    session["_strawberryid.email"]      = data["email"]
    session["_strawberryid.full_name"]  = data["full_name"]
    session["_strawberryid.avatarurl"]  = data["profile_picture_url"]
    
    return redirect(f"/{redir_lang}")
    

# Logout
@app.route("/logout", defaults={'lang': 'en'}, methods=['GET', 'POST'])
@app.route('/<string:lang>/logout', methods=['GET', 'POST'])
async def logout(lang):
    session.pop('_strawberryid.username', None)
    session.pop('_strawberryid.password', None)
    session.pop('_strawberryid.avatarurl', None)
    session.pop('_strawberryid.full_name', None)

    return redirect(f"/{lang}")


# Account page
@app.route("/account", defaults={'lang': 'en'})
@app.route('/<string:lang>/account')
def account(lang):
    def StringLoader(str):
        return strloader(lang, str)
    
    is_authenticated = False
    view_type = request.args.get('v', default=False)
    
    if not view_type:
        return js_screen_size_script
        
    if not logged_in(session):
        print("You must be logged in")
        return redirect(f"/{lang}/login")

    if logged_in(session):
        db = sql.connect('backend/data.db')
        c = db.cursor()
        
        username = session.get("_strawberryid.username")
        profile_picture_url = session.get("_strawberryid.avatarurl")
        name = session.get("_strawberryid.full_name")
        is_authenticated = True
        
        # c.execute('SELECT cloud_engine_enabled FROM users WHERE username = ? AND password = ?', (session.get("_strawberryid.username"), session.get("_strawberryid.password")))
        c.execute('SELECT cloud_engine_enabled FROM users WHERE username = ?', (session.get("_strawberryid.username"),))
        result = c.fetchall()
        allowed_ce = result[0]
        
    else:
        username, profile_picture_url, name, allowed_ce = None, None, None, "false" 
        
    return render_template('account.html',
                           loader=StringLoader,
                           lang=lang,
                           is_authenticated=is_authenticated,
                           username=username,
                           profile_picture_url=profile_picture_url,
                           account_name=name,
                           view_type=view_type,
                           allowed_ce=allowed_ce[0])



if __name__ == "__main__":
    app.run(host=ip_address, port=port, debug=debug_mode, threaded=threaded)
    