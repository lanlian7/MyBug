from bs4 import BeautifulSoup
import urllib
import urllib2

#for some video from yangshengtang,html:http://www.39yst.com/yst/

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
        
class Video(Base):
    __tablename__='video'
    
    ID=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(100),nullable=False)
    Contents=db.Column(db.String(200),nullable=False)
    Url=db.Column(db.String(300),nullable=False)
    Img=db.Column(db.String(200))
    Count=db.Column(db.String(40))
    ReleaseTime=db.Column(db.String(50))

class subTemp():
    def __init__(self,url,title,img):
        self.url=url
        self.title=title
        self.img=img
        

listItem=[]
soup=BeautifulSoup(urllib.urlopen('http://www.39yst.com/yst/'),"lxml")
tags = soup.find(class_='ztb')
for ztb in tags.find_all(class_='tuimg'):
    for a in ztb.find_all('a'):
        url=a.get('href')
        subsoup=BeautifulSoup(urllib.urlopen(url),"lxml")
        murl=subsoup.find('iframe').get('src')
        title=a.get('title')
        img = a.find('img').get('src')
        subtemp=subTemp(murl,title,img)
        listItem.append(subtemp)

i=0 
for weizi in tags.find_all(class_='wenzi'):  
    list1=weizi.find_all('p')
    substr = list1[1].get_text()
    content=list1[2].get_text()
    count=list1[1].get_text()[:9]
    releaseTime=list1[1].get_text()[15:31]
    temp=listItem[i]
    video=Video(Title=temp.title,Img=temp.img,Url=temp.url,Contents=content,Count=count,ReleaseTime=releaseTime)
    db.session.add(video)
    i+=1


         
         

if __name__=='__main__':
    db.session.commit()      
    
    
    
    