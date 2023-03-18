from ..utils import db
from enum import Enum


class CourseName(Enum):
    MATHEMATICS="mathematics"
    ENGLISH = "english"
    SCIENCE = "science"
    HISTORY = "history"
    PHYSICAL_EDUCATION = "physical_education"
    SOCIAL_STUDIES = "social_studies"
    ART = "art"
    COMPUTER_SCIENCE = "computer_science"
    NONE = "none"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key = True)
    course_name = db.Column(db.Enum(CourseName), nullable = False, default = CourseName.NONE)
    name = db.Column(db.String(45), nullable = False, unique= True)
    email = db.Column(db.String(50), nullable= False, unique= True)
    password_hash = db.Column(db.Text(), nullable = False)
    regcourse = db.relationship("RegCourse", backref="user", lazy=True)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

