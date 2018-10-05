import sys
import database
from database import db
from  sqlalchemy.sql.expression import func
import random


first_names = ["Bob", "Edward", "Jane", "Maria", "Susan", "Nick"]
last_names = ["Hendricks", "Norrington", "Doe", "Sullivan", "Brice", "Henry"]
project_name_prefix = ["Incredible", "Fantastic", "Big", "Magic", "Better"]
project_name_suffix = ["Leap", "Jump", "Revolution", "World", "Configuration"]

if __name__ == "__main__":

    employees = []

    # Create few employees
    for i in range(0, 10):
        employee = database.Employee()
        employee.firstname = random.choice(first_names)
        employee.lastname = random.choice(last_names)
        employee.division = "business" if (i % 2 == 0) else "coder"

        employees += [employee]
        db.session.add(employee)
        db.session.commit()

    # Create few projects
    for i in range(0, 4):
        project = database.Project()
        project.name = "{prefix} {suffix}".format(prefix=random.choice(project_name_prefix),
                                                  suffix=random.choice(project_name_suffix))
        db.session.add(project)
        db.session.commit()

    # Assign few employees to project
    projects = database.Project.query.all()
    for project in projects:
        project_manager = database.Employee.query\
            .filter_by(division="business")\
            .order_by(func.random())\
            .first()
        project_employees = database.Employee.query\
            .filter_by(division="coder")\
            .order_by(func.random())\
            .limit(5)\
            .all()
        project.employees = [project_manager] + project_employees
        db.session.add(project)
        db.session.commit()

    sys.exit(0)
