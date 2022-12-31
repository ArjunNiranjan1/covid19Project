from flask import Flask, render_template
from sqlalchemy import create_engine
from app.casesImage import save_to, plot

app = Flask(__name__)

'''
clouddb = 'cockroachdb://Arjun:ZTP0gR_dTDFPapT53EySTw@chief-wallaby-3959.6zw.cockroachlabs.cloud:26257/covid19-project?sslmode=verify-full'

try:
    engine = create_engine(clouddb)
    status = "good"
except:
    status = "bad"
'''
t1 = save_to

#plot()

status = "hm"
@app.route('/')
def home():
    return render_template("landing.html", t1 = t1, status = status)

if __name__ == '__main__':
    app.run()