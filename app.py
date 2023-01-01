from flask import Flask, render_template
from application.casesImage import read, plot, save_to
import os

app = Flask(__name__)

t0 = save_to

t1 = os.getcwd()
#c = read()
#plot()

path = t1 + '/requirements.txt'
f = open(path, 'r')
c = f.read()
f.close()


@app.route('/')
def home():
    return render_template("landing.html", t0 = t0, t1 = t1, t2 = c)

if __name__ == '__main__':
    app.run()