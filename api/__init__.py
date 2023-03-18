from flask import Flask
from .auth.views import auth_namespace
from .student.views import student_namespace
from .course.views import course_namespace
from flask_restx import Api
from .config.config import config_dict
from .utils import db
from .models.user import User
from .models.student import Student
from .models.course import RegCourse
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


# initialization of flask_restx
def create_app(config = config_dict['dev']):
    app= Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)
    migrate = Migrate(app, db)


    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize"
        }
    }

    api = Api(
        app,
        title='Student Management API',
        description='A simple Student Management REST API service',
        authorizations=authorizations,
        security='Bearer Auth'
        )
    api.add_namespace(auth_namespace)
    api.add_namespace(student_namespace)
    api.add_namespace(course_namespace)

    @app.shell_context_processor
    def make_shell_context():
        return{
            "db":db,
            "User":User,
            "Student":Student,
            "RegCourse": RegCourse,
        }

    
    return app