from flask import Flask, render_template
from application.casesImage import read, plot
import os

app = Flask(__name__)

#c = read()
#plot()


@app.route('/')
def home():
    return render_template("landing.html")

if __name__ == '__main__':
    app.run()