import flask

app = flask.Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route("/")
def index():
    from database import Employee
    employees = Employee.query.all()
    return flask.render_template("home.html.jinja2", employees=employees)


@app.route("/new_employee")
def generate_for_new_employee():
    return flask.render_template("employee_form.html.jinja2")


@app.route("/testing_form")
def testing_parameters_in_form():
    return flask.render_template("employee_form.html.jinja2",
                                 firstname="Donald",
                                 lastname="Duck",
                                 division="coder",
                                 employee_id=1)


@app.route("/test_db")
def test_db():
    from database import Employee
    all_employees = Employee.query.all()
    maria_hendricks = Employee.query.filter(Employee.firstname == "Maria")\
                                    .filter_by(lastname="Hendricks")\
                                    .first()
    business_employees = Employee.query.filter_by(division="business").all()

    print("pause")

    from database import Employee, db
    new_employee = Employee()
    new_employee.firstname = "Bob"
    new_employee.lastname = "Douglas"
    new_employee.division = "coder"
    db.session.add(new_employee)
    db.session.commit()  # Send the data to the database

    print("pause")

    from database import Employee, db
    bob_douglas = Employee.query.filter_by(firstname="Bob")\
                                .filter_by(lastname="Douglas")\
                                .filter_by(division="coder")\
                                .first()

    if bob_douglas is not None:
        db.session.delete(bob_douglas)
        db.session.commit()  # Send the data to the database

    print("pause")

    return "OK"


@app.route("/update_employee/<employee_id>")
def update_employee(employee_id):
    from database import Employee

    employee = Employee.query.filter_by(id=employee_id).first()

    if employee is None:
        return flask.redirect(flask.url_for("index", 404))

    return flask.render_template("employee_form.html.jinja2",
                                 firstname=employee.firstname,
                                 lastname=employee.lastname,
                                 division=employee.division,
                                 employee_id=employee.id)


@app.route("/process_employee_form", methods=["POST"])
def process_employee_form_function():
    print(flask.request.form)
    firstname = flask.request.form["firstname"]
    lastname = flask.request.form["lastname"]
    division = flask.request.form["division"]

    print("I have to process a new employee whose name is %s"
          " and %s who is working in %s" % (firstname, lastname, division))

    from database import db, Employee

    if "id" in flask.request.form:
        employee = Employee.query.filter_by(id=flask.request.form["id"]).first()
    else:
        employee = Employee()

    if employee is None:
        flask.redirect(flask.url_for("index"), 404)

    employee.firstname = firstname
    employee.lastname = lastname
    employee.division = division

    db.session.add(employee)
    db.session.commit()

    return flask.redirect(flask.url_for("index"))


if __name__ == "__main__":
    print("Running the main program")
    app.jinja_env.auto_reload = True
    app.run(host="0.0.0.0", port=5000, debug=True)
