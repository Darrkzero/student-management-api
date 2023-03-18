from flask_restx import Namespace, Resource, fields
from flask import request,jsonify
from http import HTTPStatus
from ..models.student import Student
from ..models.user import User
from ..models.course import RegCourse
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils import db
from sqlalchemy import select

course_namespace = Namespace("course", description="name space for courses")

# Define the course model
course_model = course_namespace.model('StudentCourse', {
    'id': fields.Integer(required=True, description='The student ID'),
    'course_name': fields.String(required=True, description='The course name',
    enum =["MATHEMATICS","ENGLISH","SCIENCE","HISTORY","PHYSICAL_EDUCATION","SOCIAL_STUDIES","ART","COMPUTER_SCIENCE"]),
    'teacher_name': fields.String(required=True, description='The teacher name'),
})

view_course_model = course_namespace.model('Student', {
    'id': fields.Integer(required=True, description='The course ID'),
    'course_name': fields.String(required=True, description='The course name',
    enum =["MATHEMATICS","ENGLISH","SCIENCE","HISTORY","PHYSICAL_EDUCATION","SOCIAL_STUDIES","ART","COMPUTER_SCIENCE"]),
    'teacher_name': fields.String(required=True, description='The teacher name'),
    'grade': fields.Integer(required=True, description='The student grade'),
    'student_id': fields.Integer(required=True, description='The student id'),
    'teacher_id': fields.Integer(required=True, description='The teacher id'),
})

# ["MATHEMATICS","ENGLISH","SCIENCE","HISTORY","PHYSICAL EDUCATION","SOCIAL STUDIES","ART","COMPUTER SCIENCE"]

# define the endpoint for getting all courses
@course_namespace.route('/courses')
class OrderGetCreate(Resource):

    @course_namespace.expect(course_model)
    @jwt_required()
    @course_namespace.doc(description="""
            This endpoint is accessible to only students. 
            It registers a course
            """)
    def post(self):
        """
            Register a course
        """
        email = get_jwt_identity()
        data = course_namespace.payload

        current_user = Student.query.filter_by(email=email).first()
        teacher = User.query.filter_by(name = data["teacher_name"]).first()
        # Retrieve all the emails of the students from the database
        stmt = select(Student.email)
        result_proxy = db.session.execute(stmt)
        names = [row[0] for row in result_proxy.fetchall()]

        exists = RegCourse.query.filter_by(student_id=current_user.id,course_name=data["course_name"]).first() is not None
        if email in names:
            if exists:
                return{"message":"course has been registered already"}, HTTPStatus.OK
            new_course = RegCourse(
                course_name = data["course_name"],
                teacher_name = data["teacher_name"],
                student_id = current_user.id,
                teacher_id = teacher.id
            )

            new_course.save()
            return data, HTTPStatus.CREATED
            
        return {"message":"Unauthorized user"}, HTTPStatus.UNAUTHORIZED

    
    @course_namespace.marshal_with(view_course_model)
    @jwt_required()
    @course_namespace.doc(description="""
            This endpoint is accessible to only an admin and teacher. 
            It reads all courses
            """)
    def get(self):
        """
            Get all courses
        """
        email = get_jwt_identity()
        # Retrieve all the emails of the teachers from the database
        stmt = select(User.email)
        result_proxy = db.session.execute(stmt)
        names = [row[0] for row in result_proxy.fetchall()]
        if email in names:
            courses = RegCourse.query.all()
            return courses, HTTPStatus.OK
        
        return {"message":"Unauthorized user"}, HTTPStatus.UNAUTHORIZED

# define the endpoint for getting all courses by student id
@course_namespace.route('/course/<int:student_id>')
class OrderGetCreate(Resource):
    @course_namespace.marshal_with(view_course_model)
    @jwt_required()
    @course_namespace.doc(description="""
            This endpoint is accessible to only the student with the student id. 
            It reads all courses by student id
            """)
    def get(self, student_id):
        """
            Get all student grades by student id
        """
        email = get_jwt_identity()
        student = Student.query.filter_by(email=email).first()
        if student.id == student_id:

            grades = RegCourse.query.filter_by(student_id=student_id).all()

            return grades, HTTPStatus.OK
        
        return {"message":"Unauthorized user"}, HTTPStatus.UNAUTHORIZED
    

# define the endpoint for getting all courses by course name
@course_namespace.route('/course/<string:course_name>')
class OrderGetCreate(Resource):
    @course_namespace.marshal_with(view_course_model)
    @jwt_required()
    @course_namespace.doc(description="""
            This endpoint is accessible to only the teacher of the course. 
            It reads all courses by course name
            """)
    def get(self, course_name):
        """
            Get specific all courses by course name
        """
        email = get_jwt_identity()
        # student_email = []
        teacher = User.query.filter_by(email=email).first()
        course = RegCourse.query.filter_by(course_name=course_name.upper()).first()
        courses = RegCourse.query.filter_by(course_name=course_name.upper()).all()

        if teacher and teacher.name == course.teacher_name:
            return courses, HTTPStatus.OK
        
        return {"message":"Unauthorized user"}, HTTPStatus.UNAUTHORIZED
            
        

