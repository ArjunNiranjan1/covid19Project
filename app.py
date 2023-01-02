from flask import Flask, render_template
from application.summary import connect, get_df, cases

app = Flask(__name__)

@app.route('/')
def home():
    data = get_df(connect())
    c = cases(data)
    plot = f'data:image/png;base64,{c}'
    return render_template("landing.html", content = plot)

'''
@app.route('/fig')
def page2():
    data = get_df(connect())
    out = plot(data)
    return f"<img src='data:image/png;base64,{out}'/>"
'''
if __name__ == '__main__':
    app.run()
    
    
