#coding=utf-8

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import random

#for some daily food methods

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
    
from bs4 import BeautifulSoup
import urllib
import urllib2

soup=BeautifulSoup(urllib.urlopen('http://www.cnys.com/caipu/').read(),"lxml")
subsoup=soup.find(class_="submenu")
class Menu():
    def __init__(self,href,title):
        self.href=href
        self.title=title

list=[]

EffectList=[
    '含有大量胶原蛋白，很多女性都知道胶原蛋白可使皮肤细腻，光滑有弹性。所以这么好的胶原蛋白的来源一定不要放过哦。',
    '含有很多脂肪，但其脂肪都是不饱和脂肪酸，不容易存储的。常吃可改变血液的酸性，对防治酒糟鼻有特效的哦。',
    '含有丰富的维生素C，以及其他很多矿物质，女性常吃会使自己红润有光泽但要注意不要空腹吃',
    '不仅可以防病，常吃苹果还可以使皮肤柔润、亮白',
    '不含脂肪，且利尿，并能有效阻止糖类转化为脂肪，是女性减肥圣品。',
    '肉皮含丰富的胶原蛋白和弹性蛋白，是一种低价高营养的美容益寿佳品。女性常吃可以减缓衰老，皮肤红润有弹性。',
    '含有丰富的蛋白质、且脂肪和胆固醇含量低。作为肉类食品，它是最佳选择。常吃可有效淡斑，并避免肥胖。',
    '强身健体，提高免疫力，补肾精，促进智力发育',
    '肝中铁质丰富，是补血食品中最常用的食物。尤其是猪肝，其营养含量是猪肉的十多倍。食用猪肝可调节和改善贫血病人造血系统的生理功能。',
    '黄豆营养丰富，含有小儿生长发育必需的优质蛋白、钙、磷、铁和维生素，其营养价值能与肉、蛋、鱼相媲美。',
    ]

for a in subsoup.find_all('a'):
    href=a.get('href')
    title=a.get('title')
    menu=Menu(href,title)
    list.append(menu)
# i=0
# for h1 in soup.find_all('h1'):
#     kinds=h1.get_text()
#     print h1
#     tags=h1.find('ul')
#     print tags
#     print kinds
#     for tag in tags.find_all('li'):
#         i+=1
#         for subtag in tag.find_all('a'):
#             url=subtag.get('href')
#             title=subtag.get('title')
#             for sub in tag.find_all('img'):
#                 Img=sub.get('src')
#                 Cai=Caipu(Url=url,Title=title,Img=Img)
#                 db.session.add(Cai)
 
i=0
j=0
caipcate=soup.find(class_="caipcate")
for tags in caipcate.find_all('ul'):
    j=j+1
    for tag in tags.find_all('li'):
        temp=random.randint(0,9)
        for subtag in tag.find_all('a'):
            url=subtag.get('href')
            title=subtag.get('title')
            for sub in tag.find_all('img'):
                Img=sub.get('src')
                Cai=Caipu(Url=url,Title=title,Img=Img,kinds=list[j].title,Effect=EffectList[temp])
                db.session.add(Cai)   
 
         
if __name__=='__main__':
    db.session.commit()
    
    