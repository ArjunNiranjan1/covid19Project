from flask import Flask, render_template
from application.summary import connect, get_df, plot, save_to

app = Flask(__name__)

plot(get_df(connect()))

@app.route('/')
def home():
    return render_template("landing.html", save_to = save_to)

if __name__ == '__main__':
    app.run()