from flask import Flask
from config import config
from flask.templating import render_template

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('WEB/TEMPLATES/auth/login.html')

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run()