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



class RegCourse(db.Model):
    __tablename__ = "regcourses"
    id = db.Column(db.Integer(), primary_key = True)
    course_name = db.Column(db.Enum(CourseName), nullable = False)
    teacher_name = db.Column(db.String(50), nullable= False)
    grade = db.Column(db.Integer(), nullable= False, default=0)
    student_id = db.Column(db.Integer(), db.ForeignKey("students.id"),nullable= False)
    teacher_id = db.Column(db.Integer(), db.ForeignKey("users.id"),nullable= False)

    def __repr__(self) -> str:
        return f"<User {self.course_name}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


