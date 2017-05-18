from bs4 import BeautifulSoup
import urllib
import urllib2
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
# for unique foods make method
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'I Love C++!',
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:041166@localhost:3306/myserver',
    'SQLALCHEMY_COMMIT_ON_TEARDOW': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
})

db = SQLAlchemy(app)
Base=db.Model

class Caipu(Base):
    __tablename__='caipu'
    
    ID=db.Column(db.Integer,primary_key=True)
    Url=db.Column(db.String(200))
    Title=db.Column(db.String(200))
    Img=db.Column(db.String(200))
    kinds=db.Column(db.String(100))
    Materials = db.relationship('Material', backref='Caipu', lazy='dynamic')
    methodss=db.relationship('Methods',backref='Caipu',lazy='dynamic')
    
class Material(Base):
    __tablename__='Material'    
    
    ID = db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50))
    Number=db.Column(db.String(50))
    CaipuID=db.Column(db.Integer,db.ForeignKey(Caipu.ID))
        
class Methods(Base):
    __tablename__='methods'
    ID=db.Column(db.Integer,primary_key=True)
    Src=db.Column(db.String(200))
    Gif=db.Column(db.String(200))
    Title=db.Column(db.String(200))
    Content=db.Column(db.String(200))
    CaipuId=db.Column(db.Integer,db.ForeignKey(Caipu.ID))
    

i=0
for row in Caipu.query.limit(20).offset(0).all():
    soup1=BeautifulSoup(urllib.urlopen(row.Url),"lxml")
    tags=soup1.find(class_='tujie')
    for tag in tags.find_all('span'):
        src=tag.find('img').get('src')
        gif=tag.find('img').get('data-original')
        title=tag.find('b').get_text().split(' ')
        for p in tag.find_all('p'):
            content=p.get_text()
            if content!="":
                i+=1
                method=Methods(Src=src,Gif=gif,Title=title[1],Content=content,CaipuId=row.ID)
                db.session.add(method)
                        

if __name__=='__main__':
    db.session.commit()
    

            
