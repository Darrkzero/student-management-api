import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.user import User
from ..models.course import RegCourse
from flask_jwt_extended import create_access_token
from ..models.student import Student


def student():
    # Create a student user and add them to the database
        student = Student(id=1, email="student@test.com",name="testUser", password_hash="password")
        db.session.add(student)
        db.session.commit()
        token = create_access_token(identity=student.email)
        headers={
            "Authorization": f"Bearer {token}"
        }
        return headers

def teacher_or_admin():
      # Create a teacher user and add them to the database
        teacher = User(email="teacher@test.com",name="testuser", password_hash="password", course_name= "NONE")
        db.session.add(teacher)
        db.session.commit()
        token = create_access_token(identity=teacher.email)
        headers={
            "Authorization": f"Bearer {token}"
        }
        return headers

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()
        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None
        
# test for signup user 
    def test_user_registration(self):

        data = {
            "name": "testuser",
            "email": "testuser@gmail.com",
            "course_name":"ART",
            "password": "password"
        }

        response = self.client.post('/auth/signup/user', json=data)

        user = User.query.filter_by(email='testuser@gmail.com').first()
        assert user.name == "testuser"
        assert response.status_code == 201

# test for signup student 
    def test_student_registration(self):
        data = {
            "name": "testuser",
            "email": "testuser@gmail.com",
        }

        response = self.client.post('/auth/signup/student', json=data)

        student = Student.query.filter_by(email='testuser@gmail.com').first()
        assert student.name == "testuser"
        assert response.status_code == 201

# test for login user 
    def test_user_login(self):
        data = {
            "email": "testuser@gmail.com",
            "password": "password"
        }
        response = self.client.post('/auth/login/user', json=data)

        assert response.status_code == 200

# test for login student 
    def test_student_login(self):
        data = {
            "email": "testuser@gmail.com",
            "password": "password"
        }
        response = self.client.post('/auth/login/student', json=data)

        assert response.status_code == 200

# test for changing password 
    def test_reset_password(self):
            headers= student()

            data = {
                 "old_password":"password",
                 "new_password":"new_password"
            }

            response = self.client.patch("/auth/reset_password",json=data, headers=headers)
            assert response.status_code == 200