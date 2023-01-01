from flask import Flask, render_template
from application.casesImage import read, plot, save_to
import os

app = Flask(__name__)

t0 = round((9*8)/3,2)

t1 = os.getcwd()
#c = read()
#plot() desktop/arjun/projects


f = open('covid19Project/root.crt', 'r')
c = f.read()
f.close()


@app.route('/')
def home():
    return render_template("landing.html", t0 = t0, t1 = t1, t2 = len(c))

if __name__ == '__main__':
    app.run()