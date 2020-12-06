from flask import Flask, url_for, render_template, request, session, redirect, flash
import database
import secrets

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.readSecret('secretkey')

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        username = session.get("username")
        password = session.get("password")
        if database.authenticate(username, password):
            user = database.get_todos(session["username"])

            return render_template('signedin.html',
                username = session["username"],
                todos = user['todos'],
                num_of_todos = len(user['todos']))
        else:
            session["username"] = ""
            session["password"] = ""
            return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if database.username_taken(username):
            if database.authenticate(username, password):
                session["username"] = username
                session["password"] = password
                return redirect(url_for('index'))
            else:
                flash("Incorrect username or password")
                return redirect(url_for('login'))

        else:
            flash(f'{username} does not exist, please create an account')
            return redirect(url_for('signup'))

    return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    elif request.method == "POST":
        if request.form.get("ageCheck"):
            if request.form["password1"] != request.form["password2"]:
                flash('passwords do not match')
                return redirect(url_for('signup'))

            elif database.username_taken(request.form["username"]):
                flash('username has been taken')
                return redirect(url_for('signup'))

            else:
                session["username"] = request.form["username"]
                session["password"] = request.form["password1"]
                database.add_user(request.form["username"], request.form["password1"])
                flash(database.account_creation_status(request.form["username"], request.form["password1"]))
                return redirect(url_for('index'))

        else:
            flash('You must be at least 13 years old to sign up')
            return redirect(url_for('signup'))

@app.route('/addtodo')
def add_todo():
    todo = request.args["todo"]
    database.submit_todo(todo, session["username"])
    return redirect(url_for('index'))

@app.route('/remove_todo', methods=["GET", "POST"])
def removetodo():
    database.remove_todo(request.form["todoname"], session["username"])
    return redirect(url_for('index'))
        

@app.route('/logout')
def logout():
    session["username"] = ""
    session["password"] = ""
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)