from flask import Flask, render_template
from application.casesImage import read, plot, save_to

app = Flask(__name__)

t1 = save_to
c = read()
plot()

@app.route('/')
def home():
    return render_template("landing.html", t1 = t1, t2 = len(c))

if __name__ == '__main__':
    app.run()