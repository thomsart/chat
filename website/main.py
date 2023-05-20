from flask import Flask, render_template, redirect, url_for, session


app = Flask(__name__)
app.secret_key = "3gf5h/.4j65f414-j65315/fgh35rdt+1h54rtd1hbns"
NAME_KEY = "name"


@app.route("/login")
def login():
    return render_template("")


@app.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))


@app.route("/")
def home():
    # if NAME_KEY not in session:
    #     return redirect(url_for("login"))
    return render_template("home.html", name=home)


if __name__ == "__main__":
    app.run(debug=True)