from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_image_alchemy.storages import S3Storage
from flask_image_alchemy.fields import StdImageField
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
s3_storage = S3Storage()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = 0
    isActive = 0
    image = db.Column(
        StdImageField(
            storage=s3_storage,
            variations={
                'thumbnail': {"width": 100, "height": 100, "crop": True}
            }
        )
    )
    date = db.Column(db.DateTime, default=datetime.utcnow)

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