# Web Shop application & API

This is the introduction to my web shop implementation. It consists of two parts: web application and API. Let's see what you can do with each of them.

### Prerequisites

I used some extra packages for this project, so you'll need to install them as well in order to run it. Those packages are listed in the _requirements.txt_ file.

##### MySQL

As a database, I used MySQL, and as I started the server locally, you'll also have to configure it on your machine. It's pretty simple, just follow the steps below:

1. Istallation
    1. Make sure you have `mysql-server` installed
    2. You'll also need some extra packages: `python3-dev libmysqlclient-dev default-libmysqlclient-dev`
    3. Finally, install `mysqlclient` via `pip`
2. Creating database
    1. Log in to MySQL root using command `sudo mysql -u root` (add `-p` if you've set a password)
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

### Models

The main models are __ShopUser__ and __Shop__ itself. Shop has name, shop_id, and can have one or many owners. Users have one of the types - USER or ADMIN. USER can only see his profile and nothing else, and ADMIN can perform all the CRUD operations on ShopUsers and Shops.
By default, newly created user has type USER. To change it, you can create superuser (`python manage.py createsuperuser`). His type will bes set to ADMIN by default. Also, if you log in to admin panel with the superuser's credentials, you'll be able to make any other user an ADMIN.

### API

API is implemented using Django REST framework. It's pretty basic realization of CRUD operations on the main models.

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

allowed: ADMIN

---

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

allowed: ADMIN

---

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

allowed: ADMIN


### Web application

This part is implemented on Django itself. For the front-end I used Bootstrap 4 and crispy forms. Let's see the pages you can interact with!

#### Common views

These are pages that can be accessed regardless of account type.

##### Sign up

Before you can see the website's content, an account should be created. From any page being accessed without authorization, you'll be redirected to login form. There, if you don't have an account yet, press the _Sign up_ button at the bottom of the page. It will get you to this view:

![Signup page](https://i.imgur.com/RBnYaGi.png)

Fill the fields with your email, pick up a password and press the _Sign up_ button. A new account will be created and you'll be redirected to the login page.

##### Log in

Since your account is created, you can log in to the system using your credentials.

![Login page](https://i.imgur.com/DxH1bBV.png)

After that, you'll see the home page.

##### Home page

There's a navigation bar on top of the page. If your account type is USER, the only available view is your profile.

![Home page](https://i.imgur.com/nQi5lBW.png)

##### Log out

To log out, press the corresponding button on the right side of the navbar. You'll be logged out from the system and redirected to the login page.

##### Your profile

To see your account details, visit your profile page. The button is on the right side of the navbar. There, you can see the list of the shops that you own (if you do).

![Your profile page](https://i.imgur.com/izqY8XW.png)

### Admin views

These are pages that can be accessed only by accounts of ADMIN type. Two extra buttons will apper on the left side of navbar:

![Admin panel buttons](https://i.imgur.com/z0JmZ14.png)

##### Users list

By pressing the _Users_ button, you can see all of the registered users with number of shops owned by each:

![Users page](https://i.imgur.com/Dhm3rTz.png)

##### User profile

You can see any user details, and also edit or delete the account.

![User profile page](https://i.imgur.com/0tAf7fl.png)

![Edit user page](https://i.imgur.com/snzVwo6.png)

##### Shops list

The same way you can see the registered shops,

![Shops page](https://i.imgur.com/KVUNeYf.png)

add a new one,

![Add shop page](https://i.imgur.com/nK6Z11b.png)

and also edit or delete the existing ones:

![Shop details page](https://i.imgur.com/MsntbVF.png)

---

That's it! Go ahead and ckeck it yourself :)
