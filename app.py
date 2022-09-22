from flask import Flask, render_template, url_for, request, redirect
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
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=True)
    image = db.Column(
        StdImageField(
            storage=s3_storage,
            variations={
                'thumbnail': {"width": 100, "height": 100, "crop": True}
            }
        )
    )
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.title
        # return f"<item {self.id}>"

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', title='Главная страница', data=items)

@app.route('/about')
def about():
    return render_template('about.html', title='about')

@app.route('/create', methods=['POST','GET'])
def create():
    if request.method == 'POST':
        title=request.form['title']
        price=request.form['price']
        # text=request.form['text']

        item = Item(title=title, price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "добавление не удалось"
    else:
        return render_template('create.html', title='Добавление товара')

@app.route('/new_page')
def new_page():
    return render_template('new_page.html', title='new page')


if __name__ == '__main__':
    app.run(debug=True)