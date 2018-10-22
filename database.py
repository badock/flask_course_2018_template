from flask_sqlalchemy import SQLAlchemy
from webapp import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


association_table = db.Table('association',
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)

    division = db.Column(db.Text)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    employees = db.relationship('Employee', secondary=association_table, lazy='subquery',
        backref=db.backref('projects', lazy=True))
