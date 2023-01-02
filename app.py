from flask import Flask, render_template
from application.summary import connect, get_df, plot

app = Flask(__name__)

plot(get_df(connect()))

@app.route('/')
def home():
    return render_template("landing.html")

if __name__ == '__main__':
    app.run()