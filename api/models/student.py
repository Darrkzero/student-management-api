from ..utils import db

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(45), nullable = False)
    email = db.Column(db.String(50), nullable= False, unique= True)
    password_hash = db.Column(db.Text(), nullable = False)
    gpa = db.Column(db.Integer(), nullable = False, default= 0)
    graded = db.Column(db.Boolean(), default = False)
    regcourses = db.relationship("RegCourse", backref="student", lazy=True)


    def __repr__(self) -> str:
        return f"<User {self.name}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()