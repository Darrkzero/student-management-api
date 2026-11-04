
# Student Management API

<p style="font-size:20px;">The Student Management API is a REST API that allows teachers to grade their students, allows students to register their courses, allows admin calculate the students gpa and many other functions. 
<!-- It is built with Flask and Flask-restx and can be accessed through https://darrkzero.pythonanywhere.com/, a PythonAnywhere-powered web app -->
</p>

<div></div>

<h1>Note</h1>
["MATHEMATICS","ENGLISH","SCIENCE","HISTORY","PHYSICAL EDUCATION","SOCIAL STUDIES","ART","COMPUTER SCIENCE"]                    
  <br>Only the list of courses above can be registered and the admin email must be "admin@gmail.com"

<h1>Prerequisites</h1>
Python version: Python 3.10.10
<div></div>  
<h1>Installation</h1>
<div></div>
<ul style="font-size:18px;">
    <li>Clone the repository to your local machine.</li>
    <li>Navigate to the project directory.</li>
    <li>Create a virtual environment and activate it:</li>
    <li>Install the dependencies:</li>
    <li>Copy <code>.env.example</code> to <code>.env</code> and set <code>SECRET_KEY</code> and <code>JWT_SECRET_KEY</code> to long random values:</li>
    <li>Run the application:</li>
</ul>

```console
python -m venv venv
source venv/bin/activate
```

```console
pip install -r requirements.txt
```

```console
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
```

```console
python runserver.py
```

<p style="font-size: 20px; margin-top: 20px;">To start operations with the database and navigate through some API endpoints ... the user to the endpoints will have to be authorized by making use of the model of login and signup and its authentication. There are different authorizations for teachers and students.</p>




# EndPoints For Student Management API

<div style="margin-top:8px; margin-bottom:10px; font-size:20px; font-weight:bold;">Auth EndPoint</div>
<!-- Tables for routing in each models -->

| ROUTE                     | METHOD | DESCRIPTION                                     | AUTHORIZATION          | USER TYPE         |
| ------------------------  | ------ | ----------------------------------------------- | ---------------------- | ---------         |
| `/auth/signup/user`   | _POST_ | Creation of teachers or admin account           | `None`                 | teachers or admin |
| `/auth/signup/student`| _POST_ | Creation of students account                    | `None`                 | students          |
| `/auth/login/user`    | _POST_ | Creation of JWT Tokens for teachers or admin    | `None`                 | teachers or admin |
| `/auth/login/student` | _POST_ | Creation of JWT Tokens for students             | `None`                 | Students          |
| `/auth/refresh`       | _POST_ | Creation of Refresh Tokens for all account      | `Bearer Refresh-Token` | Any               |
| `/auth/reset_password`| _PATCH_| Change password                                 | `Bearer Refresh-Token` | Any               |


<div style="margin-top:20px; margin-bottom:10px; font-size:20px; font-weight:bold;">Student EndPoint</div>

| ROUTE                                                       | METHOD  | DESCRIPTION                           | AUTHORIZATION         | USER TYPE         |
| ----------------------------------------------------------- | ------  | ------------------------------------- | --------------------- | ----------------- |
| `/student/students`                                     | _GET_   | Get all students info                 | `Bearer Access-Token` | teachers or admin |
| `/student/student/<int:student_id>`                     | _PATCH_ | Update Student Info by student id     | `Bearer Access-Token` | Student           |
| `/student/student/<int:student_id>`                     | _DELETE_| Delete Student Info by student id     | `Bearer Access-Token` | teachers or admin |
| `/student/students/<string:course_name>`                | _GET_   | Get Student Info by course name       | `Bearer Access-Token` | course teacher    |
| `/student/student/<string:course_name>/<int:student_id>`| _PATCH_ | Grade Student course                  | `Bearer Access-Token` | course teacher    |
| `/student/gpa/<int:student_id>`                         | _PATCH_ | Calclate Students gpa By student Id   | `Bearer Access-Token` | Admin             |

<div style="margin-top:20px; margin-bottom:10px; font-size:20px; font-weight:bold;">Course EndPoint</div>

| ROUTE                                     | METHOD | DESCRIPTION                   | AUTHORIZATION         | USER TYPE         |
| ----------------------------------------- | ------ | ----------------------------  | --------------------- | ---------------   |
| `/course/courses`                     | _POST_ | Register a Course             | `Bearer Access-Token` | Student           |
| `/course/courses`                     | _GET_  | Get all course                | `Bearer Access-Token` | teachers or admin |
| `/course/course/<int:student_id>`     | _GET_  | Get all course by student id  | `Bearer Access-Token` | student           |
| `/course/course/<string:course_name>` | _GET_  | Get all course by course name | `Bearer Access-Token` | course teacher    |

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/Darrkzero/student-management-api/blob/main/LICENSE">LICENSE</a> for more information.


---
