from app import db


class BlogPost(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return '<title {}'.format(self.title)

class Employee(db.Model):

    __tablename__ = "Employee"

    EmployeeID = db.Column(db.String, primary_key=True)
    FirstName = db.Column(db.String, nullable=False)
    LastName = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)

    def __init__(self, FirstName, LastName, EmailAddress, Password, EmployeeID):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Password = Password
        self.EmployeeID = EmployeeID
