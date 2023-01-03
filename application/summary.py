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
    q = 'SELECT cases.date, cases.dailycases, deaths.dailydeaths FROM cases FULL JOIN deaths ON cases.date=deaths.date;'
    df = pd.read_sql_query(q, con)
    df = df.fillna(0)
    return df

def cases(df):
    fig = Figure()
    ax = fig.subplots()
    
    ax.plot(df["date"],df["dailycases"],color='purple')
    ax.set_title("COVID-19 cases in England",loc="left",weight="bold")
    ax.set_xlabel("Date",weight="bold")
    ax.set_ylabel("Cases",weight="bold")
    ax.set_xticks(df["date"][list(range(0,len(df),int(round(len(df)/5,0))))])
    ax.invert_xaxis()
    
    buf = BytesIO()
    fig.savefig(buf, format='png')
    out = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return out

def deaths(df):
    fig = Figure()
    ax = fig.subplots()
    
    ax.plot(df["date"],df["dailydeaths"],color='red')
    ax.set_title("Deaths",loc="left",weight="bold")
    ax.set_xlabel("Date",weight="bold")
    ax.set_ylabel("Death Count",weight="bold")
    ax.set_xticks(df["date"].iloc[[*list(range(0,len(df),int(round(len(df)/5,0)))),len(df)-1]])
    ax.invert_xaxis()

    buf = BytesIO()
    fig.savefig(buf, format='png')
    out = base64.b64encode(buf.getbuffer()).decode('ascii')
    
    return out

def mortality(df):
    fig = Figure()
    ax = fig.subplots()
    
    ax.plot(df["date"],df["dailydeaths"]/df["dailycases"],label="Death Rate",color='red')
    ax.set_ylim(0,1)
    ax.legend()
    ax.set_title("Mortality over time",loc="left",weight="bold")
    ax.set_xlabel("Date",weight="bold")
    ax.set_ylabel("Mortality",weight="bold")
    ax.set_xticks(df["date"].iloc[[*list(range(0,len(df),int(round(len(df)/5,0)))),len(df)-1]])

    buf = BytesIO()
    fig.savefig(buf, format='png')
    out = base64.b64encode(buf.getbuffer()).decode('ascii')
    
    return out

def hist1(df):
    return None

def hist2(df):
    return None