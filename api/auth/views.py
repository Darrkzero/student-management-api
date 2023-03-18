from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from ..models.user import User
from ..models.student import Student
from ..utils import db
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import random
import string


def generate_password(length):
    # define the set of characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation

    # generate the password by randomly selecting characters from the set
    password = ''.join(random.choice(characters) for i in range(length))

    return password


auth_namespace = Namespace("auth", description="name space for authentication")

# signup model for both admin and teachers
signup_model = auth_namespace.model(
    "SignupUser",{
        "name": fields.String(required =True, description = "A name"),
        "email": fields.String(required =True, description = "An email"),
        "course_name":fields.String(required =True, description = "course name",
        enum =["NONE","MATHEMATICS","ENGLISH","SCIENCE","HISTORY","PHYSICAL_EDUCATION","SOCIAL STUDIES","ART","COMPUTER_SCIENCE"]),
        "password":fields.String(required =True, description = "A password")
    }
)

# signup model for students
student_signup_model = auth_namespace.model(
    "SignupStudent",{
        "name": fields.String(required =True, description = "A name"),
        "email": fields.String(required =True, description = "An email"),
    }
)


view_model = auth_namespace.model(
    "User",{
        "id":fields.Integer(),
        "name": fields.String(required =True, description = "A name"),
        "email": fields.String(required =True, description = "An email"),
        "course_name":fields.String(required =True, description = "course name"),
        "password_hash":fields.String(required =True, description = "A password"),
    }
)


# login model for all users
login_model = auth_namespace.model(
    "LoginStudent",{
        "email": fields.String(required =True, description = "An email"),
        "password":fields.String(required =True, description = "A password")
    }
)

password_model  = auth_namespace.model(
    "Password",{
        "old_password": fields.String(required =True, description = "old password"),
        "new_password":fields.String(required =True, description = "new password")
    })

# endpoint for registering both admin and teachers
@auth_namespace.route("/signup/user")
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(view_model)
    @auth_namespace.doc("Register admin or teacher")
    def post(self):
        """
        Signup a user
        """
        data = request.get_json()
        new_user = User(
            name = data.get("name"),
            email = data.get("email"),
            course_name = data.get("course_name"),
            password_hash = generate_password_hash(data.get("password"))
        )
        new_user.save()
        return new_user,HTTPStatus.CREATED
    
# endpoint for registering both admin and teachers
@auth_namespace.route("/signup/student")
class SignUp(Resource):

    @auth_namespace.expect(student_signup_model)
    @auth_namespace.doc("Register student")
    def post(self):
        """
        Signup a student
        """
        new_password = generate_password(10)
        data = request.get_json()
        new_user = Student(
            name = data.get("name"),
            email = data.get("email"),
            password_hash = generate_password_hash( new_password)
        )
        new_user.save()

        display_user = {
            'id' : new_user.id,
            'name' :data.get("name"),
            'email' : data.get("email"),
            'password' : new_password
        }
        return display_user,HTTPStatus.CREATED

@auth_namespace.route("/login/user")
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
        Login an admin or a teacher
        """
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")
        user = User.query.filter_by(email=email).first()
        
        if user is not None and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity = user.email)
            refresh_token = create_refresh_token(identity = user.email)
            response = {
                "access_token":access_token,
                "refresh_token":refresh_token
            }

            return response, HTTPStatus.CREATED


@auth_namespace.route("/login/student")
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
        Login a student
        """
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        student = Student.query.filter_by(email=email).first()
        if student is not None and check_password_hash(student.password_hash, password):
            access_token = create_access_token(identity = student.email)
            refresh_token = create_refresh_token(identity = student.email)
            response = {
                "access_token":access_token,
                "refresh_token":refresh_token
            }
            return response, HTTPStatus.CREATED

@auth_namespace.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        username= get_jwt_identity()
        access_token = create_access_token(identity=username)
        return{"access_token": access_token}, HTTPStatus.OK
    
@auth_namespace.route("/reset_password")
class Refresh(Resource):
    @jwt_required()
    @auth_namespace.expect(password_model)
    def patch(self):
        """
        change password
        """
        email= get_jwt_identity()

        data = request.get_json()
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        student = Student.query.filter_by(email=email).first()
        user = User.query.filter_by(email=email).first()
        if student is not None and check_password_hash(student.password_hash, old_password):
            student.password_hash = generate_password_hash( new_password)
            db.session.commit()
        elif user is not None and check_password_hash(student.password_hash, old_password):
            user.password_hash = generate_password_hash( new_password)
            db.session.commit()

        return{"message":"password changed successfully"}, HTTPStatus.OK