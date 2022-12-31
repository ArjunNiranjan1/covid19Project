from flask import Flask, render_template
import application.casesImage

app = Flask(__name__)
t1 = application.casesImage.save_to
t2 = len(application.casesImage.cases)

@app.route('/')
def home():
    return render_template("landing.html", t1 = t1, t2 = t2)

if __name__ == '__main__':
    app.run()