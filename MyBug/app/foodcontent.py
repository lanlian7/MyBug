#coding=utf-8
from bs4 import BeautifulSoup
import urllib

import sys   
reload(sys) # Python2.5 鍒濆鍖栧悗浼氬垹闄?sys.setdefaultencoding 杩欎釜鏂规硶锛屾垜浠渶瑕侀噸鏂拌浇鍏?  
sys.setdefaultencoding('utf-8')   

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'I Love C++!',
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:041166@localhost:3306/myserver?charset=utf8',
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
    foodItem = db.relationship('FoodItem', backref='TypeItem', lazy='dynamic')

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
    
class FoodItem(Base):
    __tablename__='foodItem'
    
    ID=db.Column(db.Integer,primary_key=True)
    TypeItemID=db.Column(db.Integer,db.ForeignKey(TypeItem.ID))
    Url=db.Column(db.String(200))
    Name=db.Column(db.String(200))
    Img=db.Column(db.String(200))
    FoodContents = db.relationship('FoodItemContent', backref='FoodItem', lazy='dynamic')
    FoodMethods = db.relationship('FoodItemMethod', backref='FoodItem', lazy='dynamic')  
    FoodImgs = db.relationship('FoodItemImg', backref='FoodItem', lazy='dynamic')  
    
class FoodItemContent(Base):
    __tablename__='foodItemContent'
    
    ID=db.Column(db.Integer,primary_key=True)
    Content=db.Column(db.String(500))
    Ingredients=db.Column(db.String(500))#涓绘枡
    Accessories=db.Column(db.String(500))#杈呮枡
    FoodItemID=db.Column(db.Integer,db.ForeignKey(FoodItem.ID))
    
class FoodItemMethod(Base):
    __tablename__='foodItemMethod'
    
    ID=db.Column(db.Integer,primary_key=True)
    Method=db.Column(db.String(500))
    FoodItemID=db.Column(db.Integer,db.ForeignKey(FoodItem.ID))
    
class FoodItemImg(Base):
    __tablename__='foodItemImg'
    
    ID=db.Column(db.Integer,primary_key=True)
    Img=db.Column(db.String(200))
    FoodItemID=db.Column(db.Integer,db.ForeignKey(FoodItem.ID))

for row in FoodItem.query.limit(50).offset(0).all():
    soup=BeautifulSoup(urllib.urlopen(row.Url),"lxml")
    print row.Url
    subsoup=soup.find(class_='content')
    i=0
    content=''
    Ingredients=''
    accessories=''
    if subsoup is None:
        continue
    for p in subsoup.find_all('p'):
        text=p.get_text()
        i=i+1
        if i==2:
            content=text
        elif i==4:
            ingredients=text
        elif i==5:
            accessories=text
        elif i==1 or i==3 or text.find(unicode("秋季助消化食谱草莓山药").encode("utf-8"))!=-1 or text.find(unicode("步骤").encode("utf-8"))!=-1:
            continue
        elif p.find('img') is not None:
            img=p.find('img').get('src')
            foodImg=FoodItemImg(Img=img,FoodItemID=row.ID)
            db.session.add(foodImg)
        elif text is not None  and text!= "":
            foodmethod=FoodItemMethod(Method=text,FoodItemID=row.ID)
            db.session.add(foodmethod)
            if p.get_text().find(unicode("鎴愬搧").encode("utf-8")) != -1:
                if p.find_next('p').find('img') is not None:
                    img=p.find_next('p').find('img').get('src')
                    foodImg=FoodItemImg(Img=img,FoodItemID=row.ID)
                    db.session.add(foodImg)
                break
    foodcontent=FoodItemContent(FoodItemID=row.ID,Content=content,Ingredients=ingredients,Accessories=accessories)
    db.session.add(foodcontent) 
if __name__=='__main__':
    db.session.commit()