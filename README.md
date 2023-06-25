use with python 3.11

`python -m venv YourVirtualEnvName`

### for windows users
`YourVirtualEnvName\Scripts\activate` 

### for mac user
`source bin\activate` 


`python -m pip install -r requirements.txt`

`cd Smart Calender App`
`configure settings.py and add your postgres database information`

`python manage.py makemigrations` 

`python manage.py migrate`

`python manage.py runserver`

### REST API URL

{
    "users": "http://127.0.0.1:8000/api/users/", -- For list user (Get Request) and create user (Post Request)
    "update_user" : "http://127.0.0.1:8000/api/users/<pk:user_id>", For update user(Put Request)
    "delete_user" : "http://127.0.0.1:8000/api/users/<pk:user_id>/delete/", For delete user(Delete Request)
    "scheduler": "http://127.0.0.1:8000/api/scheduler/", For all Schedule list (Get Request) and create Schedule (Post Request)
    "analytics" : "http://127.0.0.1:8000/api/scheduler/analytics/", For show analytics (Get Request)
}

### Note: Use Basic Auth While Using RestApi through curl or postman



