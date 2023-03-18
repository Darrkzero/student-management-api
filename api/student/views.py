from flask_restx import Namespace, Resource, fields
from flask import request
from http import HTTPStatus
from ..models.student import Student
from ..models.user import User
from ..models.course import RegCourse
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils import db
from sqlalchemy import select

student_namespace = Namespace("student", description="name space for students")

# Define the student model
student_model = student_namespace.model('StudentGpa', {
    'id': fields.Integer(required=True, description='The student ID'),
    'name': fields.String(required=True, description='The student name'),
    'email': fields.String(required=True, description='The student email'),
    'password_hash': fields.String(required=True, description='The student password'),
    'gpa': fields.Float(required=True, description='The student GPA'),
    'graded':fields.Boolean(required=True, description='confirm if student is graded')
})

discreet_student_model = student_namespace.model('StudentId', {
    'id': fields.Integer(required=True, description='The student ID'),
    'name': fields.String(required=True, description='The student name'),
    'email': fields.String(required=True, description='The student email'),
    'password_hash': fields.String(required=True, description='The student password'),
})

edit_student_model = student_namespace.model('StudentEdit', {
    'id': fields.Integer(required=True, description='The student ID'),
    'name': fields.String(required=True, description='The student name'),
    'email': fields.String(required=True, description='The student email'),
})

# Define the course model
course_model = student_namespace.model('Student', {
    'id': fields.Integer(required=True, description='The student ID'),
    'course_name': fields.String(required=True, description='The course name',
    enum =["MATHEMATICS","ENGLISH","SCIENCE","HISTORY","PHYSICAL EDUCATION","SOCIAL STUDIES","ART","COMPUTER SCIENCE"]),
    'teacher_name': fields.String(required=True, description='The teacher name'),
    'grade': fields.String(required=True, description='The student grade'),
})


# Define the endpoint for getting all students
@student_namespace.route('/students')
class Students(Resource):

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description="""
            This endpoint is accessible to only an admin and teacher. 
            It reads all students
            """)
    @jwt_required()
    def get(self):
        """
            Get all students 
        """
        email = get_jwt_identity()
        # Retrieve all the emails of the teachers from the database
        stmt = select(User.email)
        result_proxy = db.session.execute(stmt)
        names = [row[0] for row in result_proxy.fetchall()]
        if email in names:

            students = Student.query.all()
            return students, HTTPStatus.OK
        return {"message":"Unauthorized user"}, HTTPStatus.UNAUTHORIZED
    
# Define the endpoint for getting a single student by id
@student_namespace.route('/student/<int:student_id>')
class UpdateOrderStatus(Resource):

    @student_namespace.expect(edit_student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description="""
            This endpoint is accessible to only the student with the student id. 
            It updates a student by student id
            """)
    @jwt_required()
    def patch(self, student_id):
        """
            Update a student's status
        """
        data = student_namespace.payload
        email = get_jwt_identity()
        # Retrieve all the emails of the teachers from the database
        stmt = select(Student.email)
        result_proxy = db.session.execute(stmt)
        names = [row[0] for row in result_proxy.fetchall()]
        if email in names:
            student = Student.query.get_or_404(student_id)
            student.name = data["name"]
            student.email = data["email"]
            db.session.commit()

            return student, HTTPStatus.OK
        return {"message":"Unauthorized user"}, HTTPStatus.UNAUTHORIZED
    

    @jwt_required()
    @student_namespace.doc(description="""
            This endpoint is accessible to only an admin and teacher. 
            It deletes student by student id
            """)
    def delete(self,student_id):
        """
            Delete a student by ID
        """
        email = get_jwt_identity()
       # Retrieve all the emails of the teachers from the database
        stmt = select(User.email)
        result_proxy = db.session.execute(stmt)
        names = [row[0] for row in result_proxy.fetchall()]
        if email in names:
            delete_order = Student.query.get_or_404(student_id)
            db.session.delete(delete_order)
            db.session.commit()
            return {"message":"student successfully deleted"}, HTTPStatus.OK

        return {"message":"Unauthorized user"}, HTTPStatus.OK
    

# define the endpoint for getting all the students by course name
@student_namespace.route('/students/<string:course_name>')
class GetSpecificCourse(Resource):
    @jwt_required()
    @student_namespace.marshal_with(discreet_student_model)
    @student_namespace.doc(description="""
            This endpoint is accessible to only the teacher of the course. 
            It reads all students by course name
            """)
    def get(self, course_name):
        """
            Get specific course students
        """
        email = get_jwt_identity()
        student_email = []
        teacher = User.query.filter_by(email=email).first()
        course = RegCourse.query.filter_by(course_name=course_name.upper()).first()
        courses = RegCourse.query.filter_by(course_name=course_name.upper()).all()
        for course in courses:
            students = Student.query.filter_by(id=course.student_id).first()
            student_email.append(students)

        if teacher and teacher.name == course.teacher_name:
            return student_email, HTTPStatus.OK
        
        return {"message":"Unauthorized user"}, HTTPStatus.UNAUTHORIZED
    

# define the endpoint for getting a student by course name and student id
@student_namespace.route('/student/<string:course_name>/<int:student_id>')
class GetSpecificCourse(Resource):
    @jwt_required()
    @student_namespace.expect(course_model)
    @student_namespace.marshal_with(course_model)
    @student_namespace.doc(description="""
            This endpoint is accessible to only the teacher of the course. 
            It update the grade in regcourse by student id and course name
            """)
    def patch(self, course_name,student_id):
        """
            Grade each course
        """
        email = get_jwt_identity()
        data = student_namespace.payload
        teachers = User.query.filter_by(email=email).first()
        course = RegCourse.query.filter_by(course_name=course_name.upper(), student_id=student_id).first()

        if teachers and teachers.name == course.teacher_name :

            course.grade = data["grade"]
            db.session.commit()
            return course, HTTPStatus.OK
        
        return{"message":"Unauthorized user"}, HTTPStatus.OK
    

@student_namespace.route('/gpa/<int:student_id>')
class UpdateOrderStatus(Resource):
    # @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description="""
            This endpoint is accessible to only an admin. 
            It updates the GPA by student id
            """)
    @jwt_required()
    def patch(self, student_id):
        """
            Update a student's GPA
        """
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        student = Student.query.get_or_404(student_id)
        courses = RegCourse.query.filter_by(student_id=student_id).all()
        # Calculate the GPA
        if user  and user.email == "admin@gmail.com":
            
            total_grade_points = 0
            for course in courses:
                if course.grade >= 90:
                    total_grade_points += 4.0
                elif course.grade >= 80:
                    total_grade_points += 3.0
                elif course.grade >= 70:
                    total_grade_points += 2.0
                elif course.grade >= 60:
                    total_grade_points += 1.0
                else:
                    total_grade_points += 0.0
            gpa = total_grade_points / len(courses)

            student.gpa = gpa
            student.graded = True

            db.session.commit()

            return student, HTTPStatus.OK
        return {"message":"Unauthorized user"}, HTTPStatus.UNAUTHORIZED

    


