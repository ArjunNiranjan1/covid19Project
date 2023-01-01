from flask import Flask, render_template
from application.casesImage import read, plot, save_to, t
import os

app = Flask(__name__)

t0 = t

t1 = os.getcwd()
#c = read()
#plot()


c = app.instance_path


@app.route('/')
def home():
    return render_template("landing.html", t0 = t0, t1 = t1, t2 = c)

if __name__ == '__main__':
    app.run()