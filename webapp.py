import flask

app = flask.Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route("/")
def index():
    return "HelloWorld!"


if __name__ == "__main__":
    # Create the DB
    from database import db
    print("creating database")
    db.create_all()
    print("database created")

    print("Running the main program")
    app.jinja_env.auto_reload = True
    app.run(host="0.0.0.0", port=5000, debug=True)
