# dev server

from flask import Flask, url_for, render_template, request, session, redirect, flash
import database
import secrets
import sys

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.readSecret('secretkey')

@app.route('/', methods=["GET", "POST"])
def index():
    try:
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
            return redirect(url_for('signup'))
    
    except:
        flash('an unknown error occured')
        print(sys.exc_info()[0])
        return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():
    try:
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
    
    except:
        flash('an unknown error occured')
        print(sys.exc_info()[0])
        return render_template('error.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    try:
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
                print(sys.exc_info()[0])
                return redirect(url_for('signup'))
    except:
        return render_template('error.html')

@app.route('/addtodo')
def add_todo():
    try:
        todo = request.args["todo"]

        if todo.replace('\n', 'a') != todo:
            flash('Todos must be one line')

        else:
            database.submit_todo(todo, session["username"])
    
    except:
        flash('An error occured submiting your todo')
        print(sys.exc_info()[0])

    return redirect(url_for('index'))

@app.route('/remove_todo', methods=["GET", "POST"])
def removetodo():
    database.remove_todo(request.form["todoname"], session["username"])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    try:
        session["username"] = ""
        session["password"] = ""
        return redirect(url_for('login'))

    except:
        flash('There was an error logging you out')
        print(sys.exc_info()[0])
        return redirect(url_for('index'))

@app.route('/errortest')
def errortest():
    try:
        raise Exception('an error has occured')

    except:
        flash('testing error page')
        print('test: ' + sys.exc_info()[0])
        return render_template('error.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    print(e)
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)