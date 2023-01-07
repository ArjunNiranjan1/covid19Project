from flask import Flask, render_template
from application.summary import plot_dict, data_dict

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("landing.html", data_dict = data_dict, plot_dict = plot_dict)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/features/')
def features():
    return render_template('features.html')

@app.route('/vaccines/')
def vaccines():
    return render_template('vaccines.html')

@app.route('/forecasting/')
def forecasting():
    return render_template('forecasting.html')

if __name__ == '__main__':
    app.run()