from flask import Flask

app = Flask(__name__)


@app.route("/")
def home(*args, **kwargs):
    print(args, kwargs)
    return "Home"


if __name__ == "__main__":
    app.run(debug=True)
