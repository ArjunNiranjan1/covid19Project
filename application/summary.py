from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from flask import send_file
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

base = os.getcwd()
cert = base + '/root.crt'
save_to = base + '/application/static/images'

user = os.getenv('DB_USER')
pw = os.getenv("DB_PASSWORD")

#Connect to db
def connect():
    clouddb = f'cockroachdb://{user}:{pw}@chief-wallaby-3959.6zw.cockroachlabs.cloud:26257/covid19-project?sslmode=verify-ca&sslrootcert={cert}'
    con = create_engine(clouddb)
    return con

#Query date, daily cases, daily deaths
def get_df(con):
    q = 'SELECT cases.date, cases.dailycases, deaths.dailydeaths FROM cases INNER JOIN deaths ON cases.date=deaths.date;'
    df = pd.read_sql_query(q, con)
    return df

#Generate plots
def plot(df):
    fig, ax = plt.subplots(figsize=(6,6))
    ax = sns.set_style(style="darkgrid")
    
    ax.plot(df["date"],df["dailycases"],color='purple')
    ax.set_title("COVID-19 cases in England")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cases")
    ax.set_xticks(df["date"][list(range(0,len(df),int(round(len(df)/5,0))))])
    
    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    
    return send_file(img, mimetype='img/png')
    
    