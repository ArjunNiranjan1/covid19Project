from flask import Flask, render_template
import application.casesImage

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("landing.html")

if __name__ == '__main__':
    app.run()