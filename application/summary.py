from sqlalchemy import create_engine
import pandas as pd
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import base64

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
    sns.set_theme()
    cases = io.BytesIO()
    
    plt.plot(df["date"],df["dailycases"],color='purple')
    plt.title("COVID-19 cases in England")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    plt.xticks(df["date"][list(range(0,len(df),int(round(len(df)/5,0))))])
    plt.savefig(cases, format='png')
    
    return base64.encodebytes(cases.getvalue()).decode('utf-8')
    
    