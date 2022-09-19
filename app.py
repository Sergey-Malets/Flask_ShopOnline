from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'

@app.route('/')
def index():
    return render_template('index.html', title='main')

@app.route('/about')
def about():
    return render_template('about.html', title='about')

@app.route('/new_page')
def new_page():
    return render_template('new_page.html', title='new page')


if __name__ == '__main__':
    app.run(debug=True)