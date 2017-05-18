from bs4 import BeautifulSoup
import urllib

#coding=utf-8
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

class ExtraQuestion(Base):
    __tablename__='extraQuestion'
    
    ID=db.Column(db.Integer,primary_key=True)
    Url=db.Column(db.String(200))
    Img=db.Column(db.String(200))
    Title=db.Column(db.String(200))
    Brief=db.Column(db.String(400))
    ExtraQuestionItems=db.relationship('ExtraQuestionItem',backref='ExtraQuestion',lazy='dynamic')

class ExtraQuestionItem(Base):
    __tablename__='extraQuestionItem'
    
    ID=db.Column(db.Integer,primary_key=True)
    Content=db.Column(db.String(500))
    ExtraQuestionID=db.Column(db.Integer,db.ForeignKey(ExtraQuestion.ID))

soup=BeautifulSoup(urllib.urlopen('http://www.ttys5.com/shanshi/shunshi'))
subsoup=soup.find(class_='page clearfix')
i=0
for a in subsoup.find_all('a'):
    href=a.get('href')
    tempsoup=BeautifulSoup(urllib.urlopen(href))
    tempsubsoup=tempsoup.find(class_='con')
    for li in tempsubsoup.find_all('li'):
        i+=1
        url=li.find('a').get('href')
        img=li.find('a').find('img').get('src')
        title=li.find('a').find('img').get('alt')
        content=li.find('div').find('p').get_text()
        extraQuestion=ExtraQuestion(Url=url,Img=img,Title=title,Brief=content)
        db.session.add(extraQuestion)
        
print i
if __name__=='__main__':
    db.session.commit()