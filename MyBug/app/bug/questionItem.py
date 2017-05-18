#coding=utf-8
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

for row in ExtraQuestion.query.all():
    soup=BeautifulSoup(urllib.urlopen(row.Url),'lxml')
    subsoup=soup.find(class_='content')
    for p in subsoup.find_all('p'):
        if p.get_text().find('相关内容介绍'.decode('utf-8'))!=-1:
            break
        if p.get_text() is None or p.get_text()=='':
            continue
        extraQuestionItem=ExtraQuestionItem(Content=p.get_text(),ExtraQuestionID=row.ID)
        db.session.add(extraQuestionItem)
if __name__=='__main__':
    db.session.commit()
