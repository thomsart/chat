from flask import Flask, render_template, url_for


app = Flask(__name__)
app.secret_key = "3gf5h4j65f414j65d4ytjrs3f2g10h35ftx1hr5tyd315fgh35rdt1h54rtd1hbnsz3211541j"


@app.route("/chat/login")
def login():
    return render_template("")


@app.route("/chat/")



@app.route("/chat/home")
def home():
    return render_template("")




if __name__ == "__main__":
    app.run(debug=True)