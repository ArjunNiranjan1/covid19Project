from flask import Flask, render_template
import application.casesImage

app = Flask(__name__)

out = application.casesImage.save_to
out2 = len(application.casesImage.cases)

@app.route('/')
def home():
    return render_template("landing.html", content = [out,out2])

if __name__ == '__main__':
    app.run()