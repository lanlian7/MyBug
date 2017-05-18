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
    Img=db.Column(db.String(200))
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
    
for row in Effect.query.all():
    soup=BeautifulSoup(urllib.urlopen(row.Url),"lxml")
    tempsoup=soup.find(class_='page')
    for a in tempsoup.find_all('a'):
        href=a.get('href')
        itemsoup=BeautifulSoup(urllib.urlopen(href),"lxml")
        subsoup=itemsoup.find(class_='tuwen_180')
        for tag in subsoup.find_all('li'):
            url=tag.find('a').get('href')
            name=tag.find('a').get('title')
            temp=tag.find('a').find('img')
            img=''
            flag=''
            if temp is None:
                flag=tag.find('a').get_text()
                name=tag.find('a').find_next('a').get('title')
                img=tag.find('a').find_next('a').find('img').get('src')
                if name is None:
                    name=tag.find('a').find_next('a').find_next('a').get('title')
            else:
                img=temp.get('src')
            p=tag.find('p')
            introduction=p.find('span').get_text()
            p=p.find_next('p')
            effect=p.get_text()
            p=p.find_next('p')
            taboo=p.get_text()
            effectitem=EffectItem(EffectID=row.ID,Flag=flag,Url=url,Name=name,Img=img,Introduction=introduction,Virtue=effect,Taboo=taboo)
            db.session.add(effectitem)
            
if __name__=='__main__':
    db.session.commit()
            