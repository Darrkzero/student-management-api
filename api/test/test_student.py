import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.user import User
from ..models.student import Student
from ..models.course import RegCourse
from flask_jwt_extended import create_access_token
from http import HTTPStatus


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
        teacher = User(email="teacher@test.com",name="testuser", password_hash="password", course_name= "MATHEMATICS")
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

# test for getting all students 
    def test_get_all_students(self):
        headers= teacher_or_admin()
    
        response = self.client.get("/student/students", headers=headers)
        assert response.status_code == 200
        assert response.json == []

# test for updating a student 
    def test_update_a_student_success(self):
        headers= student()

        data = {
            "name": "Sample",
            "email": "samplestudent@gmail.com",
            # "password": "password"
        }
        response = self.client.patch("/student/student/1", json=data, headers=headers)
        assert response.status_code == 200

    def test_update_a_student_unauthorized(self):
        headers= teacher_or_admin()

        data = {
            "name": "Sample",
            "email": "samplestudent@gmail.com",
        }
        response = self.client.patch("/student/student/1", json=data, headers=headers)
        assert response.status_code == 401
    
    # Delete a student
    def test_delete_student(self):
        new_student = Student(email="student@test.com",name="testUser", password_hash="password")
        new_student.save()
        headers= teacher_or_admin()
        response = self.client.delete(f'/student/student/{new_student.id}', headers=headers)
        assert response.status_code == 200

# Get specific course students 
    def test_get_course_students(self):
        headers= teacher_or_admin()

        new_student = Student(email="student@test.com", name="testUser", password_hash="password")
        new_student.save()

        new_course = RegCourse(course_name="MATHEMATICS", teacher_name="testuser", student_id=new_student.id, teacher_id=1)
        new_course.save()

        response = self.client.get("/student/students/mathematics", headers=headers)
        assert response.status_code == 200

# edit specific course grade 
    def test_edit_course_grade(self):
            headers= teacher_or_admin()

            new_student = Student(email="student@test.com", name="testUser", password_hash="password")
            new_student.save()

            new_course = RegCourse(course_name="MATHEMATICS", teacher_name="testuser", student_id=new_student.id, teacher_id=1)
            new_course.save()

            data = {
                 "grade":50
            }

            response = self.client.patch("/student/student/mathematics/1",json=data, headers=headers)
            assert response.status_code == 200


    def test_update_student_gpa(self):
        teacher = User(email="admin@gmail.com", name="testuser", password_hash="password", course_name= "NONE")
        db.session.add(teacher)
        db.session.commit()
        token = create_access_token(identity=teacher.email)
        headers={
            "Authorization": f"Bearer {token}"
        }


        new_student = Student(email="student@test.com", name="testUser", password_hash="password", gpa=2)
        new_student.save()
        reg_course = RegCourse(course_name="MATHEMATICS", grade=85, teacher_name="Dr. Smith", student_id=new_student.id, teacher_id=1)
        reg_course.save()
        reg_course = RegCourse(course_name="SCIENCE", grade=92, teacher_name="Dr. Johnson", student_id=new_student.id, teacher_id=2)
        reg_course.save()

        response = self.client.patch(f"/student/gpa/1", headers=headers)

        assert response.status_code == 200
        assert response.json["gpa"] == 3.5
        assert response.json["graded"] == True
            

    

        
        

