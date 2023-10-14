from flask import Flask, app, render_template
from init import *

app = Flask(__name__, static_url_path=static_url_path, static_folder=static_folder, template_folder=template_folder)

app.config['SECRET_KEY'] = secret


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host=ip_address, port=port, debug=debug_mode, threaded=threaded)