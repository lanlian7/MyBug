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


class Effect(Base):
    __tablename__='effect'
    
    ID=db.Column(db.Integer,primary_key=True)
    Type=db.Column(db.String(100),nullable=True)
    Name=db.Column(db.String(100),nullable=True)
    Url=db.Column(db.String(200),nullable=True)
    TypeItems = db.relationship('EffectItem', backref='Effect', lazy='dynamic')
    
class EffectItem(Base):
    __tablename__='effectitem'
    
    ID=db.Column(db.Integer,primary_key=True)
    EffectID=db.Column(db.Integer,db.ForeignKey(Effect.ID))
    Url=db.Column(db.String(200))
    Name=db.Column(db.String(200))
    Img=db.Column(db.String(200))
    Introduction=db.Column(db.String(200))
    Virtue=db.Column(db.String(200))
    Taboo=db.Column(db.String(200))
    Flag=db.Column(db.String(10))

soup=BeautifulSoup(urllib.urlopen('http://food.ttys5.com/index/food_list/2'),"lxml")
subsoup=soup.find(id='anothercontent2')
h=subsoup.find('h2')
for tag in subsoup.find_all('p'):
    type=h.get_text()
    for item in tag.find_all('a'):
        url=item.get('href')
        name=item.get('title')
        effect=Effect(Type=type,Name=name,Url=url)
        db.session.add(effect)
    h=h.find_next('h2')

     
if __name__=='__main__':
    db.session.commit()


