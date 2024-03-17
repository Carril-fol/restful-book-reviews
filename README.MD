<h1 align="center">Books REST API</h1>

<h4 align="center">A monolithic REST API for managing users, profiles, books, literary genres, publishers and user reviews.</h4>

<div>
  <p align="center">
    <a>
        <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python">
    </a>
    <a>
      <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green" alt="Django">
    </a>
    <a>
      <img src="https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white" alt="Django Rest Fremework">
    </a>
    <a>
      <img src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
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

#### First you have to install "pipenv", it allows the creation of the virtual environment and where the dependencies are installed.

```
In the IDLE terminal:
> pip install pipenv
```

#### Once you have installed "pipenv", you have to start it and install the dependencies:

```
In the IDLE terminal:
> pipenv shell
Launching subshell in virtual environment...
````

```
> pipenv install
````

#### This command installs all the necessary dependencies that are in the "Pipfile".

#### Once the dependencies are installed, the application is ready to start.

#### To start the server:

```
In the IDLE terminal:
> py manage.py runserver
````

> **Note:**
> Once all the previous steps are done, the application is ready to make HTTP requests from a testing program such as POSTMAN or Insomnia.


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