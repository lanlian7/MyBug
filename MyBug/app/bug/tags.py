#coding=utf-8
# 存放一些生活的常用的养生小标签，如补血登，对应html:http://www.cnys.com/zyys/
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

soup=BeautifulSoup(urllib.urlopen('http://www.cnys.com/zyys/'),"lxml")
class Tags(Base):
    __tablename__='tags'
    
    ID=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(200))
    Url=db.Column(db.String(200))

subsoup=soup.find(class_='tags')
for tag in subsoup.find_all('a'):
    title=tag.get_text()
    href=tag.get('href')
    Tag=Tags(Title=title,Url=href)
    db.session.add(Tag)
    
if __name__=='__main__':
    db.session.commit()    
     
