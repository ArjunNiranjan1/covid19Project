from flask import Flask, render_template
from application.summary import connect, get_df, plot

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("landing.html")

@app.route('/fig')
def page2():
    data = get_df(connect())
    return f"<img src='data:image/png;base64,{data}'/>"

if __name__ == '__main__':
    app.run()
    
    
