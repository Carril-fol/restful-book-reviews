<h1 align="center">Books REST API</h1>

<h4 align="center">A monolithic REST API for managing users, profiles, books, literary genres, publishers and user reviews.</h4>

<div>
  <p align="center">
    <a href="https://badge.fury.io/js/electron-markdownify">
      <img src="https://img.shields.io/badge/Django-green?style=flat-square&logo=django&logoColor=white&labelColor=%2342b883&color=%2342b883"
              alt="Django">
    </a>
    <a href="https://gitter.im/amitmerchant1990/electron-markdownify">
            <img src="https://img.shields.io/badge/Django_Rest_Framework-red?style=flat-square&logo=django&logoColor=white&labelColor=%23f95959&color=%23f95959"
                    alt="Django Rest Fremework">
    </a>
    <a href="https://saythanks.io/to/bullredeyes@gmail.com">
        <img src="https://img.shields.io/badge/Python-yellow?style=flat-square&logo=python&logoColor=white&labelColor=%235585b5&color=%23fcff82"
                alt="Python">
    </a>
  </p>
</div>

## Features 📋

### Books:

* #### Publish a book: Allows administrator users to publish a book.
* #### List of books: A list of books.
* #### Detail of books: Shows the details of a book.
* #### Update a book: Allows administrator users to modify books.
* #### Delete a book: Allows administrator users to delete books.

### Genders:

* #### Add a gender: Allows the administrator users to create genres for the publication of books.
* #### Detail a gender: Shows the details of a gender.
* #### List of genders: A list of books.
* #### Delete gender: Allows administrator users to delete genres.
* #### Update gender: Allows administrator users to update the genres of the books.

### Publishers:
        
* #### Create a publisher: Allows administrator users to create publishers for the publication of books.
* #### Detail a publisher: It shows the details of the publisher and the books that belong to it.
* #### Delete a publisher: Allows administrator users delete publishers.
* #### Update a publisher: Allows administrator users to update publisher data.
* #### List of Books from the publisher: A list of the publisher's books.

### Reviews:

* #### Create a review: Allows users to create book reviews.
* #### Delete a review: Allows users to delete their reviews.
* #### Update a review: Allows users update their reviews.
* #### List of reviews from specific book: A list of reviews of a specific book.
* #### Detail a review: Allows the visualization of the reviews

### Profiles:

* #### Create a profile: Allows the creation of profiles automatically at the time of user registration. 
* #### Update a profile: Allows you to update your corresponding profiles.
* #### Detail a profile: Allows viewing of profile data.


## Installation

#### To install this repository:

```
In the IDLE terminal:

> git clone https://github.com/Carril-fol/books-rest-api.git
```

## Configuration ⚙️

#### Once installed, you have to configure the database in the project's settings.py:

>**Note:**
> This API uses MYSQL as default, you change what you think needs to change.

#### Add the following fields: NAME, USER, PASSOWORD from your database.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '', 
        'PORT': '',
    }
}
```

#### Once you add the above fields:

````
In the IDLE terminal:

> py manage.py makemigrations

> py manage.py migrate
````````

## Launch 🚀

> **Note:**
> Since it is a REST API, it can be consulted from an external program that allows it or from a frontend application.

#### How do I check my Python version:

````
In the IDLE terminal:
> py --version
> Python 3.10.11

In Windows CMD:
c:\> py --version
c:\> Python 3.10.11
``````

#### Install Dependencies:

#### To install the dependencies you need to run 'pip install', make sure you are in the project folder and there you should be able to see the 'requirements.txt' file:

```
In the IDLE terminal:
> pip install -r requirements.txt
```

#### Start the server:

```
In the IDLE terminal:
> py manage.py runserver
````

## Frontend Connection 🖥️

#### To make the connection with the backend in the frontend, it is necessary to perform a few steps:

```
In the IDLE terminal:
> pipenv install django-cors-headers 
````

#### In settings:
```
INSTALLED_APPS = [
    ...,
    "corsheaders",
    ...,
]
````

#### Once you add the above fields:

```
MIDDLEWARE = [
    ...,
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...,
]
````

````
CORS_ALLOWED_ORIGINS = [
     "http://localhost:3000"
]
````

#### With that, it is already configured in the backend for you to use it as you wish. Now you would have to configure how you send the requests from the frontend you are using.