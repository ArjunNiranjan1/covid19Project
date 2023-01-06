from flask import Flask, render_template
from application.summary import plot_dict, data_dict

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("landing.html", data_dict = data_dict, plot_dict = plot_dict)

@app.route('/features')
def features():
    return render_template('features.html')

if __name__ == '__main__':
    app.run()