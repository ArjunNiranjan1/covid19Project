from flask import Flask, render_template
from application.summary import connect, get_df, cases

app = Flask(__name__)

#Summary plots
summary_data = get_df(connect())
c = cases(summary_data)
cases_time_series = f'data:image/png;base64,{c}'

@app.route('/')
def home():
    return render_template("landing.html", content = cases_time_series)

if __name__ == '__main__':
    app.run()
    
    
