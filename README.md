use with python 3.11

`python -m venv YourVirtualEnvName`

### for windows users
`YourVirtualEnvName\Scripts\activate` 

### for mac user
`source bin\activate` 


`python -m pip install -r requirements.txt`

`cd attendanceProject`
`configure settings.py and add your postgres database information`

`python manage.py makemigrations`  <!-- if changes in model file -->

`python manage.py migrate`

`python manage.py runserver`

