from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .articles import Article
from .archives import Archive
from . import db
import datetime
import locale
from sqlalchemy import and_
from flask_login import login_user, logout_user, login_required


globalVar2 = 34

archives = []

def getArchives(update):
    globalVar2 = 67
    
    print('before diff')
    
    if(update or len(archives) == 0):
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8') 
   # .with_entities(Article.date_publish)distinct(Article.year_publish).group_by(Article.year_publish).all()
        archives[:] = []
        for yearFound in Article.query  \
            .distinct(Article.year_publish).with_entities(Article.year_publish) \
            .order_by(Article.year_publish.desc()):
        

            print (yearFound.year_publish)
            
            yearNumber = yearFound.year_publish

            for monthFound in Article.query.filter(and_(Article.year_publish == yearFound.year_publish, Article.is_published == True))  \
	            .distinct(Article.month_publish).with_entities(Article.month_publish) \
	            .order_by(Article.month_publish.desc()):

                archive = Archive()

                archive.yearNumber = yearNumber
                archive.monthNumber = monthFound.month_publish
                archive.monthName = datetime.date(1900, int(monthFound.month_publish), 1).strftime('%B')

                monthCount = Article.query.filter(and_(Article.year_publish==yearFound.year_publish, Article.month_publish==monthFound.month_publish, Article.is_published == 
                    True)).count()
                archive.count = monthCount
                print archive.monthName
                print archive.monthNumber
                print archive.count
                archives.append(archive)

            
         
            
            print('year report finished')

        print('after diff')
    return archives
