from flask import Flask, render_template
from application.summary import connect, get_df, plot

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("landing.html")

@app.route('/cases')
def cases():
    df = get_df(connect)
    out = plot(df)
    return out

if __name__ == '__main__':
    app.run()
    
    
