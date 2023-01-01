from flask import Flask, render_template
from application.tester import read, plot

app = Flask(__name__)

c = read()
plot(c)


@app.route('/')
def home():
    return render_template("landing.html", path = len(c))

if __name__ == '__main__':
    app.run()