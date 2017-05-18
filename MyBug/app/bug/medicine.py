#coding=utf-8
from bs4 import BeautifulSoup
import urllib
import urllib2

#用于浏览存储一些养生的小知识，对应html:中医.html

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

class Medicine(Base):
    __tablename__='medicine'
    
    ID=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(200),nullable=False)
    Img=db.Column(db.String(200))
    href=db.Column(db.String(200))

soup=BeautifulSoup(urllib.urlopen('http://www.cnys.com/zyys/'),"lxml")
subsoup=soup.find(class_='newslist3')
list=[]
i=0
for img in subsoup.find_all('h5'):
    list.append( img.find('a').get('href'))
for img in subsoup.find_all('img'):
    title=img.get('alt')
    Img=img.get('src')
    medicine=Medicine(Title=title,Img=Img,href=list[i])
    db.session.add(medicine)
    
if __name__=='__main__':
    db.session.commit()
    