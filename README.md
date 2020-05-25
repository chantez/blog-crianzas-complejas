export SECRET_KEY=9OLWxND4o83j4K4iuopO
export SQLALCHEMY_DATABASE_URI=mysql://blog:info6.caez@localhost/blog

cd /home/chantez/Desktop/proyectos/blog/blog-crianzas-complejas

export FLASK_APP=blog
export FLASK_DEBUG=1

export CONFIGURATION_FILE=/home/chantez/Desktop/proyectos/blog/blog-crianzas-complejas/blog/configuration.txt
flask run


from blog import db, create_app
db.create_all(app=create_app())  

---------------------

sudo mysql -u root  -p

describe article;
drop table article;




Dec 14, 2018

---------------
instalar idioma para fechas
sudo apt-get install language-pack-es

export LC_ALL="es_ES.UTF-8"
export LC_CTYPE="es_ES.UTF-8"
sudo dpkg-reconfigure locales
sudo dpkg-reconfigure locales


import locale
locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
----------------

Proximo paso: 
- limpiar codigo
- pasar a github
- seleccionar maquina gcp y subir
	- my sql
	- python
	- flask