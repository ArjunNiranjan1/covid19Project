from flask import Flask, render_template
from application.summary import connect, get_df, plot

app = Flask(__name__)

df = get_df(connect())
cases_plot = plot(df)

@app.route('/')
def home():
    return render_template("landing.html", cases = cases_plot)

if __name__ == '__main__':
    app.run()