# Web Shop application & API

This is the introduction to my web shop implementation. I intended to create both web application (with pretty UI) and API, but for now only the second is done. I will update this file as soon as I finish, and now let's see what you can do with the API.

### API

API is implemented using Django REST framework, so you might want to install it in order to run the project. All of the required packages are described at _requirements.txt_ file. There also are some steps that you need to do before you can use the API.

#### Prerequisites

##### MySQL

As a database, I used MySQL, and as I started the server locally, you'll also have to configure it on your machine. It's pretty simple, just perform the following steps:

1. Istallation
    1. Make sure you have `mysql-server` installed
    2. You'll also need some extra packages: `python3-dev libmysqlclient-dev default-libmysqlclient-dev`
    3. Finally, install `mysqlclient` via `pip`
2. Creating database
    1. Log in to MySQL root using command `sudo mysql -u root` (add `-p` if you set a password)
    2. Run `CREATE DATABASE shop_data;` to create database
    3. Create DB user: `CREATE USER 'shopuser'@'%' IDENTIFIED WITH mysql_native_password BY 'Web-Shop123';`
    4. Provide user with access to all operations on DB: `GRANT ALL ON shop_data.* TO 'shopuser'@'%';`
    5. Sync updates by running `FLUSH PRIVILEGES;`
    6. Exit the console (`EXIT;` command)

That's it! Note that _shop_data_ is the name of the database that Django will try to connect to, using username _shopuser_ and password _Web-Shop123_. This is defined at _web_shop/my.cnf_ file. If you want to change some of this fields, don't forget to update the file respectively.

###### One more thing to mention

While working with MySQL and Django, I faced the problem with version compatibility. If you'll get errors looking like that:
```
File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/django/db/backends/mysql/base.py", line 36, in <module>
    raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3.
```
Just know that it's common issue. I found pretty good explanation [here](http://programmersought.com/article/19241784782/;jsessionid=ECBAF2C83EFD914CBEE2E811C1451AB4). Follow this tutorial if you get the same error.

#### Models

The main models are __ShopUser__ and __Shop__ itself. Shop has name, shop_id, and can have one or many owners. Users have one of the types - USER or ADMIN. USER can only see his profile and nothing else, and ADMIN can perform all the CRUD operations on ShopUsers and Shops.
By default, newly created user has type USER. To change it, you can create superuser (`python manage.py createsuperuser`). His type will bes set to ADMIN by default. Also, if you log in to admin panel with the superuser's credentials, you'll be able to make any other user an ADMIN.

#### Using the API

Now, if you could start the project sucessfully, it will run on your localhost, 8000 port by default. So, start url for all of the endpoints will be `http://127.0.0.1:8000/api/v1/`. Let's see the endpoints and what do you need to use them.

###### Signup

url: `signup/`
method: POST
body:
```
{
	"email" : "your.email@example.com",
	"password" : "your-password"
}
```
auth: none
allowed: anybody

###### Obtain auth token

url: `api-token-auth/`
method: POST
body:
```
{
	"email" : "your.email@example.com",
	"password" : "your-password"
}
```
auth: none
allowed: anybody

If you provide valid credentials of an existing user, in a response you'll receive a token. Use it for further authentication to access the data you need.

###### Users data

url: `users/`
methods: GET, POST
headers:
```
{
	"Authorization" : "Token your-token"
}
```
body (for POST method):
```
{
	"email" : "your.email@example.com",
	"password" : "your-password"
}
```
auth: token
allowed: ADMIN

url: `users/<int:id>/`
methods: GET, PUT, DELETE
headers:
```
{
	"Authorization" : "Token your-token"
}
```
body (for PUT method):
```
{
	"email" : "your.email@example.com",
	"password" : "your-password"
}
```
auth: token
allowed: USER (only if method is GET and id is the request user id), ADMIN

Note: USER can only see his own infromation, and can not modify it. ADMIN can see any user data, and also modify or delete it. Param `id` in url should correspond to real user id in database.

###### Shop data

url: `shops/`
methods: GET, POST
headers:
```
{
	"Authorization" : "Token your-token"
}
```
body (for POST method):
```
{
	"name" : "shop-name",
}
```
auth: token
allowed: ADMIN

url: `shops/<int:shop_id>/`
methods: GET, PUT, DELETE
headers:
```
{
	"Authorization" : "Token your-token"
}
```
body (for PUT method):
```
{
	"name" : "shop-name",
}
```
auth: token
allowed: ADMIN

That's it for now. I'll add screenshots with requests examples in a few days, and also an implementation of web application is yet to come. Now you can go ahead and check the API functionality yourself!