# Feedback service
### Description
REST API for feedback service (training project for Yandex Practicum). Writing down your thoughts, commenting others, express your opinion about a wide variety of works of cinema, literature, music and art. Retrieval/manipulate information via Django REST framework: quick and safe.  
### Technologies
`Python 3.9`
`Django 3.2`
`Django REST framework 3.12.4`
### How to launch project in a dev-mode
- Clone the repository
```
git clone https://github.com/antoncp/api_yamdb
``` 
- Create and activate virtual environment
```
python3.9 -m venv venv
``` 
- Install dependencies from requirements.txt file with activated virtual environment
```
pip install -r requirements.txt
``` 
- In folder with file manage.py make migrations
```
python manage.py migrate
``` 
- Populate the database with prepared .csv-files
```
python manage.py load_csvdata
```
- And execute a command to run a server
```
python manage.py runserver
```
### Examples of using REST API
You could find detailed roadmap of using REST API of this project in [api_yamdb/static/redoc.yaml](https://github.com/antoncp/api_yamdb/blob/master/api_yamdb/static/redoc.yaml)

Project has 9 major endpoints for requests:

*AUTH*
* **/api/v1/auth/signup/** New user registration
* **/api/v1/auth/token/** Getting a JWT-token

*Users*
* **/api/v1/users/** CRUD for users (admin only)
* **/api/v1/users/me/** User account operations

*Content*
* **/api/v1/categories/** CRD for categories (non-read for admin only)
* **/api/v1/genres/** CRD for genres (non-read for admin only)
* **/api/v1/titles/** CRUD for works of art (non-read for admin only)
* **/api/v1/titles/{title_id}/reviews/** CRUD for reviews
* **/api/v1/titles/{title_id}/reviews/{review_id}/comments/** CRUD for comments

Example of retrieving information about concrete post:

*Request for fetching work of art with id №1*

```
GET http://127.0.0.1:8000/api/v1/titles/1/
```

*Response*

```
{
  "id": 1,
  "name": "Звёздные войны. Эпизод 5: Империя наносит ответный удар",
  "year": 1980,
  "description": "",
  "rating": null,
  "category": {
    "name": "Фильм",
    "slug": "movie"
  },
  "genre": [
    {
      "name": "Фантастика",
      "slug": "sci-fi"
    }
  ]
}
```

### Authors
Yandex Practicum, Tatyana Belova, Ivan Novikov, Anton Chaplygin
