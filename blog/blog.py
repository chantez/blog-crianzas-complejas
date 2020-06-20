from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from .articles import Article
from . import db
from .contextBlog import getArchives
from sqlalchemy import and_
import datetime
import locale




blog = Blueprint('blog', __name__)
POST_PER_PAGE = 5


@blog.route('/mesBlog/<year>/<month>')
def monthBlog(year, month):

    
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 0, type=int)

    print year
    print month
    month2Digits = getMonth2Digits(month)
    print month2Digits
    if(page == 1 or size <= 0):
        print('count size')
        size = Article.query.filter(and_(Article.year_publish == year, Article.month_publish == month2Digits, Article.is_published == True)).count()
    else:
        print('NO count size')

    articlesFound = Article.query.filter(and_(Article.year_publish == year, Article.month_publish == month2Digits), Article.is_published == True) \
    .order_by(Article.date_created.desc())  \
    .with_entities( Article.id, Article.title, Article.htmlText, Article.description, Article.date_created, Article.date_publish, Article.year_publish,  Article.month_publish)  \
    .paginate(page=page, per_page=POST_PER_PAGE, error_out=False, max_per_page=None)

    print len(articlesFound.items)
    return handleBlogPage(page, size, articlesFound, int(year), int(month))



@blog.route('/blog')
def mainBlog():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 0, type=int)

    if(page == 1 or size <= 0):
        print('count size')
        size = Article.query.count()
    else:
        print('NO count size')

    articlesFound = Article.query.filter( Article.is_published == True).order_by(Article.date_created.desc())  \
    .with_entities( Article.id, Article.title, Article.htmlText, Article.description, Article.date_created, Article.date_publish)  \
    .paginate(page=page, per_page=POST_PER_PAGE, error_out=False, max_per_page=None)

    print len(articlesFound.items)
    return handleBlogPage(page, size, articlesFound, 0, 0)



@blog.route('/about')
def about():
    return render_template('about.html', selected = 'about')



@blog.route('/contact')
def contact():
    return render_template('contact.html', selected = 'contact')

@blog.route('/single')
def single():

    id = request.args.get('id', type=int)

    print(id)
    article = Article.query.filter_by(id=id).first()
    
    return render_template('single.html', selected = 'blog', article=article, archives=getArchives(False))

def handleBlogPage(page, size, articlesFound, year, month):
    


    if(year > 0 and month > 0):
        next_url = url_for('blog.monthBlog', year=year, month=month, page=articlesFound.next_num) \
            if articlesFound.has_next else None

        prev_url = url_for('blog.monthBlog', year=year, month=month, page=articlesFound.prev_num) \
            if articlesFound.has_prev else None
    else:
        next_url = url_for('blog.mainBlog', page=articlesFound.next_num) \
            if articlesFound.has_next else None

        prev_url = url_for('blog.mainBlog', page=articlesFound.prev_num) \
            if articlesFound.has_prev else None

    totalPages = size / POST_PER_PAGE

    print 'size'
    print size
    if(size % POST_PER_PAGE != 0):
        totalPages = totalPages + 1

    print(totalPages)

    pageOptions = []
    if (page == 0 or page == 1 or page == 2 or page == 3):
        
        counter = 1
        while(counter <= totalPages and counter <= 5):
            pageOptions.append(counter)
            counter = counter + 1
    elif(page == totalPages or page == (totalPages - 1) or page == (totalPages - 2)):
        counter = totalPages
        while(counter  > 0 and counter > totalPages - 5):
            pageOptions.insert(0,counter)
            counter = counter - 1
    else:
        counter = page - 2
        while(counter <= totalPages and counter <= page + 2):
            pageOptions.append(counter)
            counter = counter + 1

    print pageOptions
    
    monthStr = ''
    if(month > 0):
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8') 
        monthStr = datetime.date(1900, month, 1).strftime('%B');

    print (len(getArchives(False)))
    return render_template('blog.html', selected = 'blog', articlesFound=articlesFound.items, next_url=next_url, prev_url=prev_url, size=size, page=page, pageOptions=pageOptions, archives=getArchives(False), year=year, month=month, monthStr=monthStr)



def getMonth2Digits(month):

    if(len(str(month)) == 2 ):
        return str(month)
    elif(month >= 1 or month <= 9):
        return '0' + month
    else:
        return str(month)