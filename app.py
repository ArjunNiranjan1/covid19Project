from flask import Flask, render_template
from application.summary import connect, get_df, cases, deaths, mortality, full_hist, split_hist

app = Flask(__name__)

#Summary plots
#Summary data
summary_data = get_df(connect())
#Cases time series and path string for html
c = cases(summary_data)
cases_time_series = f'data:image/png;base64,{c}'
#Deaths time series and path string for html
d = deaths(summary_data)
deaths_time_series = f'data:image/png;base64,{d}'
#Mortality time series and path string for html
m = mortality(summary_data)
mort_plot = f'data:image/png;base64,{m}'
#Histogram of daily death count (full)
f = full_hist(summary_data)
full_plot = f'data:image/png;base64,{f}'
#Histograms of daily death counts (split)
s = split_hist(summary_data)
split_plot = f'data:image/png;base64,{s}'

@app.route('/')
def home():
    return render_template("landing.html", cases_time_series = cases_time_series, deaths_time_series = deaths_time_series, mort_plot = mort_plot, full_plot = full_plot, split_plot = split_plot)

if __name__ == '__main__':
    app.run()
    
    
