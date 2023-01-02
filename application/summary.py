from sqlalchemy import create_engine
import pandas as pd
from matplotlib.figure import Figure
import seaborn as sns
import os
from io import BytesIO
import base64

sns.set_theme(style="darkgrid")

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

def plot(df):
    fig = Figure()
    ax = fig.subplots()
    
    ax.plot(df["date"],df["dailycases"],color='purple')
    
    buf = BytesIO()
    fig.savefig(buf, format='png')
    out = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return out