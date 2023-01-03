from flask import Flask, render_template
from application.summary import connect, get_df, cases, deaths, mortality

app = Flask(__name__)

#Summary plots
summary_data = get_df(connect())
c = cases(summary_data)
cases_time_series = f'data:image/png;base64,{c}'
d = deaths(summary_data)
deaths_time_series = f'data:image/png;base64,{d}'
m = mortality(summary_data)
mort_plot = f'data:image/png;base64,{m}'

@app.route('/')
def home():
    return render_template("landing.html", cases_time_series = cases_time_series, deaths_time_series = deaths_time_series, mort_plot = mort_plot)

if __name__ == '__main__':
    app.run()
    
    
