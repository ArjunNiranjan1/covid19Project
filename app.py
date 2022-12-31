from flask import Flask, render_template
from sqlalchemy import create_engine
from application.casesImage import save_to, plot

app = Flask(__name__)

clouddb = 'cockroachdb://Arjun:ZTP0gR_dTDFPapT53EySTw@chief-wallaby-3959.6zw.cockroachlabs.cloud:26257/covid19-project?sslmode=verify-full'
engine = create_engine(clouddb)

t1 = save_to
plot()

@app.route('/')
def home():
    return render_template("landing.html", t1 = t1)

if __name__ == '__main__':
    app.run()