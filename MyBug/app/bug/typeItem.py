#coding=utf-8
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

#用于存储一些食物分类

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
    


for row in Type.query.all():
    soup=BeautifulSoup(urllib.urlopen(row.Url),"lxml")
    tempsoup=soup.find(class_='page')
    for a in tempsoup.find_all('a'):
        href=a.get('href')
        itemsoup=BeautifulSoup(urllib.urlopen(href),"lxml")
        subsoup=itemsoup.find(class_='tuwen_180')
        for tag in subsoup.find_all('li'):
            url=tag.find('a').get('href')
            name=tag.find('a').get('title')
            img=tag.find('a').find('img').get('src')
            p=tag.find('p')
            introduction=p.find('span').get_text()
            p=p.find_next('p')
            effect=p.get_text()
            p=p.find_next('p')
            taboo=p.get_text()
            typeitem=TypeItem(typeID=row.ID,Url=url,Name=name,Img=img,Introduction=introduction,Virtue=effect,Taboo=taboo)
            db.session.add(typeitem)
               
if __name__=='__main__':
    db.session.commit()