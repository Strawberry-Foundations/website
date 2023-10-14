from flask import Flask, render_template, request
from init import *


app = Flask(__name__, static_url_path=static_url_path, static_folder=static_folder, template_folder=template_folder)

app.config['SECRET_KEY'] = secret



@app.route("/", defaults={'lang': 'en'})
@app.route('/<string:lang>')
def index(lang):        
    def StringLoader(str):
        return strloader(lang, str)
        
    return render_template('index.html', loader=StringLoader)


if __name__ == "__main__":
    app.run(host=ip_address, port=port, debug=debug_mode, threaded=threaded)