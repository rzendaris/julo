# Julo Test

> "I know that I know nothing" - Plato

---

#### Step 1: Create Virtual Environment
#### This project is based on Python 3.6

##### MacOs / Linux
```
$ python3 -m venv venv
```
##### Windows
```
$ py -m venv venv
```
---
#### Step 2: Start shell within our python virtual environment

##### MacOs / Linux
```
$ source venv/bin/activate
```
##### Windows
```
$ .\venv\Scripts\activate
```
---
#### Step 3: Installing packages
```
$ pip install -r requirements.txt 
```
---
#### Step 4: Initialize database scripts (run migrations before flask)
##### Create new DB
```
$ python manage.py create_db
```
##### Create new Directory in Migrations folder
```
$ mkdir migrations/versions
```
##### Model Migration
```
$ python manage.py db migrate
$ python manage.py db upgrade
```
---
#### Step 5: Run flask application
```
$ python manage.py runserver
```
---
#### Run all tests
```
$ pytest
```

#### Run a single test
```
$ pytest project_path/test_abc.py
$ pytest tests/services/test_comment_service.py
```

#### How to view all url endpoints
```
$ python manage.py shell
>>> app.url_map
```