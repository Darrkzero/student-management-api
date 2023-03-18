import unittest
from unittest.mock import patch
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.user import User
from ..models.student import Student
from ..models.course import RegCourse
from flask_jwt_extended import create_access_token
from http import HTTPStatus
from ..utils import db

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

# test for getting all courses 
    def test_get_all_courses_success(self):
        headers= teacher_or_admin()
   
        response = self.client.get("/course/courses", headers=headers)
        assert response.status_code == 200
        assert response.json == []

    def test_get_all_courses_unauthorized(self):
        headers=student()
        
        response = self.client.get("/course/courses", headers=headers)
        assert response.status_code == 401

# test for registering a course
    def test_to_register_course_success(self):
        user = User(name="Test Teacher", email="test@teacher.com", password_hash="password",course_name= "NONE")
        user.save()
        data = {
                "course_name" : "test course",
                "teacher_name" : "Test Teacher",
        }
        
        headers=student()
        response = self.client.post("/course/courses",json=data, headers=headers)

        assert response.status_code == 201

# test for getting a student courses       
    def test_get_student_grades_success(self):
        headers= student()
    
        response = self.client.get("/course/course/1", headers=headers)
        assert response.status_code == 200
        assert response.json == []


# test for getting all courses by course name
    def test_get_course_success(self):
        headers= teacher_or_admin()
        new_student = Student(email="student@test.com", name="testUser", password_hash="password")
        new_student.save()

        new_course = RegCourse(course_name="MATHEMATICS", teacher_name="testuser", student_id=new_student.id, teacher_id=1)
        new_course.save()
    
        response = self.client.get("/course/course/mathematics", headers=headers)
        assert response.status_code == 200
        assert response.json[0]["teacher_name"] == "testuser"


