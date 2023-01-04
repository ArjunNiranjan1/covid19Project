from sqlalchemy import create_engine
import pandas as pd
from matplotlib.figure import Figure
import seaborn as sns
import os
from io import BytesIO
import base64
import numpy as np

sns.set_theme(style="darkgrid")

base = os.getcwd()
cert = base + '/root.crt'

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
    
    ax.plot(df["date"],df["dailydeaths"]/df["dailycases"],color='red')
    ax.set_ylim(0,1)
    ax.set_title("Mortality over time",loc="left",weight="bold")
    ax.set_xlabel("Date",weight="bold")
    ax.set_ylabel("Mortality",weight="bold")
    ax.set_xticks(df["date"].iloc[[*list(range(0,len(df),int(round(len(df)/5,0)))),len(df)-1]])
    ax.invert_xaxis()

    buf = BytesIO()
    fig.savefig(buf, format='png')
    out = base64.b64encode(buf.getbuffer()).decode('ascii')
    
    return out

def full_hist(df):
    fig = Figure()
    ax = fig.subplots()
    
    ax.hist(df["dailydeaths"],color="red")
    ax.set_title("Distribution of daily death counts",loc="left",weight="bold")
    ax.set_xlabel("Death count",weight="bold")
    ax.set_ylabel("Frequency",weight="bold")
    
    buf = BytesIO()
    fig.savefig(buf, format='png')
    out = base64.b64encode(buf.getbuffer()).decode('ascii')
    
    return out

def split_hist(df):
    fig = Figure()
    ax = fig.subplots()
    
    ax.hist(df["dailydeaths"][500:],color="red",alpha=0.5,label="First 523 days")
    ax.hist(df["dailydeaths"][:500],color="red",alpha=1,label="Recent 500 days")
    ax.set_ylim(0,700)
    ax.set_title("Distribution of daily death counts,\nsplit 500 days ago",loc="left",weight="bold")
    ax.set_xlabel("Death count",weight="bold")
    ax.set_ylabel("Frequency",weight="bold")
    ax.legend()
    
    buf = BytesIO()
    fig.savefig(buf, format='png')
    out = base64.b64encode(buf.getbuffer()).decode('ascii')
    
    return out

#Summary plots
#Summary data
summary_data = get_df(connect())

#Cases time series and path string for html
c = cases(summary_data)
cases_time_series = f'data:image/png;base64,{cases(summary_data)}'

#Deaths time series and path string for html
d = deaths(summary_data)
deaths_time_series = f'data:image/png;base64,{d}'

#Mortality time series and path string for html
m = mortality(summary_data)
mort_plot = f'data:image/png;base64,{m}'

#Histogram of daily death count (full)
f = full_hist(summary_data)
full_plot = f'data:image/png;base64,{f}'

#Histograms of daily death counts (split)
s = split_hist(summary_data)
split_plot = f'data:image/png;base64,{s}'

data_dict = {}
data_dict["dayOfMaxDeaths"] = summary_data["date"][summary_data["dailydeaths"]==max(summary_data["dailydeaths"])]
data_dict["fullMortality"] = round(np.mean(summary_data["dailydeaths"]/summary_data["dailycases"]),2)
data_dict["earlyMortality"] = round(np.mean(summary_data["dailydeaths"][:200]/summary_data["dailycases"][:200]),2)
data_dict["lateMortality"] = round(np.mean(summary_data["dailydeaths"][200:]/summary_data["dailycases"][200:]),2)