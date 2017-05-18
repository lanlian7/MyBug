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

class Caipu(Base):
    __tablename__='caipu'
    
    ID=db.Column(db.Integer,primary_key=True)
    Url=db.Column(db.String(200))
    Title=db.Column(db.String(200))
    Img=db.Column(db.String(200))
    kinds=db.Column(db.String(100))
    Effect=db.Column(db.String(300))
    Materials = db.relationship('Material', backref='Caipu', lazy='dynamic')
    Methodss=db.relationship('Methods',backref='Caipu',lazy='dynamic')

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
    
class Video(Base):
    __tablename__='video'
    
    ID=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(100),nullable=False)
    Contents=db.Column(db.String(200),nullable=False)
    Url=db.Column(db.String(300),nullable=False)
    Img=db.Column(db.String(200))
    Count=db.Column(db.String(40))
    ReleaseTime=db.Column(db.String(50))
    
class Medicine(Base):
    __tablename__='medicine'
    
    ID=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(200),nullable=False)
    Img=db.Column(db.String(200))
    href=db.Column(db.String(200))

class Tags(Base):
    __tablename__='tags'
    
    ID=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(200))
    Url=db.Column(db.String(200))


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
    foodItem = db.relationship('FoodItem', backref='TypeItem', lazy='dynamic')

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
    Ingredients=db.Column(db.String(500))#主料
    Accessories=db.Column(db.String(500))#辅料
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

db.drop_all()
db.create_all()
    

    
    