from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .articles import Article
from . import db
import datetime
import locale
from .contextBlog import getArchives


crudBlog = Blueprint('crudBlog', __name__)
POST_PER_PAGE = 5

@crudBlog.route('/listBlog')
@login_required
def listBlog():
    print('before query')
    
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 0, type=int)

    if(page == 1 or size <= 0):
        print('count size')
        size = Article.query.count()
    else:
        print('NO count size')


    print(size)

    
    articlesFound = Article.query.order_by(Article.date_created.desc())  \
    .with_entities( Article.id, Article.title, Article.htmlText, Article.description, Article.date_created, Article.date_publish, Article.is_published)  \
    .paginate(page=page, per_page=POST_PER_PAGE, error_out=False, max_per_page=None)

    print(articlesFound)
    
    next_url = url_for('crudBlog.listBlog', page=articlesFound.next_num) \
        if articlesFound.has_next else None

    prev_url = url_for('crudBlog.listBlog', page=articlesFound.prev_num) \
        if articlesFound.has_prev else None

    totalPages = size / POST_PER_PAGE

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
    
    return render_template('crudBlog.html', selected = 'listBlog', articlesFound=articlesFound.items, next_url=next_url, prev_url=prev_url, size=size, page=page, pageOptions=pageOptions)



@crudBlog.route('/createBlog')
@login_required
def createBlog():
    print('crating query')
    
    return render_template('createBlog.html', selected = 'createBlog')

@crudBlog.route('/createBlog', methods=['POST'])
@login_required
def createBlog_post():
    title = request.form.get('title')
    description = request.form.get('description')
    htmlText = request.form.get('htmlText')
    isPublished = request.form.get('isPublished')
    dateCreated = datetime.datetime.now()
    datePublish = None
    isPublishedInt = 0
    monthPublish = None
    yearPublish = None

    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

    print(dateCreated.strftime('%b %d %Y'))
    print(title)
    print(description)
    print(htmlText)
    if isPublished:
        datePublish = datetime.datetime.now()
        isPublishedInt = 1
        monthPublish = datePublish.strftime('%m')
        yearPublish = datePublish.strftime('%Y')
        print('Publicado')
    else:
        print('No Publicado')
    
    print(yearPublish)
    print(monthPublish)


    newArticle = Article(title=title, htmlText=htmlText, description=description, is_published=isPublishedInt, \
        date_created=dateCreated, date_publish=datePublish, \
        year_publish=yearPublish, month_publish=monthPublish)

    # add the new user to the database
    db.session.add(newArticle)
    db.session.commit()
    getArchives(True)
    flash('Blog created')



    return redirect(url_for('crudBlog.listBlog'))


@crudBlog.route('/editBlog')
@login_required
def editBlog():
    print('editing query')

    id = request.args.get('id', type=int)

    print(id)
    article = Article.query.filter_by(id=id).first()
    
    print(article)
    return render_template('editBlog.html', selected = 'editBlog', article=article)

@crudBlog.route('/editBlog', methods=['POST'])
@login_required
def editBlog_post():
    title = request.form.get('title')
    id = request.args.get('id', type=int)
    description = request.form.get('description')
    htmlText = request.form.get('htmlText')
    isPublished = request.form.get('isPublished')
    datePublish = None
    isPublishedInt = 0

    print(title)
    print(id)
    print(description)
    print(htmlText)
   

    articleToUpdate = Article.query.filter_by(id=id).first()
    
    articleToUpdate.title = title;
    articleToUpdate.description = description;
    articleToUpdate.htmlText = htmlText;

    if((articleToUpdate.is_published == None or articleToUpdate.is_published == 0 ) and isPublished):
        articleToUpdate.date_publish = datetime.datetime.now()
        articleToUpdate.is_published = 1
        articleToUpdate.month_publish = articleToUpdate.date_publish.strftime('%m')
        articleToUpdate.year_publish = articleToUpdate.date_publish.strftime('%Y')


    if(not isPublished):
        articleToUpdate.is_published = 0

    # add the new user to the database
    db.session.commit()

    flash('Blog created')

    getArchives(True)
    return redirect(url_for('crudBlog.listBlog'))
