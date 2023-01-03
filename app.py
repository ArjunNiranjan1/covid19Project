from flask import Flask, render_template
from application.summary import cases_time_series, deaths_time_series, mort_plot, full_plot, split_plot

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("landing.html", cases_time_series = cases_time_series, deaths_time_series = deaths_time_series, mort_plot = mort_plot, full_plot = full_plot, split_plot = split_plot)

if __name__ == '__main__':
    app.run()