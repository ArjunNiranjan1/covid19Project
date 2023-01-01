from flask import Flask, render_template
from application.tester import read, plot

app = Flask(__name__)

c = read()
#plot()


@app.route('/')
def home():
    return render_template("landing.html", test = len(c[0]), path = c[1])

if __name__ == '__main__':
    app.run()