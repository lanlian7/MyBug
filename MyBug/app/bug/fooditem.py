from bs4 import BeautifulSoup
import urllib
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'I Love C++!',
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:041166@localhost:3306/myserver',
    'SQLALCHEMY_COMMIT_ON_TEARDOW': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
})

db = SQLAlchemy(app)
Base=db.Model

class Type(Base):
    __tablename__='Type'
    
    ID=db.Column(db.Integer,primary_key=True)
    Item=db.Column(db.String(100),nullable=True)
    Name=db.Column(db.String(100),nullable=True)
    Url=db.Column(db.String(200),nullable=True)
    Img=db.Column(db.String(200))
    TypeItem = db.relationship('TypeItem', backref='Type', lazy='dynamic')


class TypeItem(Base):
    __tablename__='typeitem'
    
    ID=db.Column(db.Integer,primary_key=True)
    typeID=db.Column(db.Integer,db.ForeignKey(Type.ID))
    Url=db.Column(db.String(200))
    Name=db.Column(db.String(200))
    Img=db.Column(db.String(200))
    Introduction=db.Column(db.String(200))
    Virtue=db.Column(db.String(200))
    Taboo=db.Column(db.String(200))

class FoodItem(Base):
    __tablename__='foodItem'
    
    ID=db.Column(db.Integer,primary_key=True)
    TypeItemID=db.Column(db.Integer,db.ForeignKey(TypeItem.ID))
    Url=db.Column(db.String(200))
    Name=db.Column(db.String(200))
    Img=db.Column(db.String(200))

for row in TypeItem.query.limit(50).offset(0).all():
    soup=BeautifulSoup(urllib.urlopen(row.Url),"lxml")
    subsoup=soup.find(class_='ul_ten clearfix')
    for tag in subsoup.find_all('li'):
        url=tag.find('a').get('href')
        name=tag.find('a').get('title')
        img=tag.find('a').find('img').get('src')
        foodItem=FoodItem(TypeItemID=row.ID,Url=url,Name=name,Img=img)
        db.session.add(foodItem)

        
if __name__=='__main__':
    db.session.commit()
    print 'success'