#imports
from sqlalchemy import create_engine
import pandas as pd
from matplotlib.figure import Figure
import seaborn as sns
import os
from io import BytesIO
import base64
import datetime
import numpy as np
from scipy import stats

#stuff
sns.set_theme(style="darkgrid")

base = os.getcwd()
cert = base + '/root.crt'

user = os.getenv('DB_USER')
pw = os.getenv("DB_PASSWORD")

plots_vac = {}
data_vac = {}
pop = 55_980_000

#connect
def connect():
    clouddb = f'cockroachdb://{user}:{pw}@chief-wallaby-3959.6zw.cockroachlabs.cloud:26257/covid19-project?sslmode=verify-ca&sslrootcert={cert}'
    con = create_engine(clouddb)
    return con

#get_df
def get_df(con):
    q = 'SELECT cases.date, cases.dailycases, deaths.dailydeaths, vaccinations.dailyfirsts, vaccinations.dailyseconds, vaccinations.dailythirds, vaccinations.cumseconds FROM cases FULL JOIN deaths ON cases.date=deaths.date FULL JOIN vaccinations ON cases.date=vaccinations.date;'
    df = pd.read_sql_query(q, con)
    df = df.fillna(0)
    return df

#time series
def time_series(df):
    fig = Figure()
    ax = fig.subplots()
    
    ax.plot(df["date"],df["dailyfirsts"],color="blue",label="First doses")
    ax.plot(df["date"],df["dailyseconds"],color="green",label="Second doses")
    ax.plot(df["date"],df["dailythirds"],color="orange",label="Boosters")
    ax.set_title("Vaccinations",loc="left",weight="bold")
    ax.set_xlabel("Date",weight="bold")
    ax.set_ylabel("Vaccination Count",weight="bold")
    ax.legend()
    ax.set_xticks(df["date"][list(range(0,len(df),int(round(len(df)/5,0))))])
    ax.invert_xaxis()
    
    buf = BytesIO()
    fig.savefig(buf, format='png')
    out = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return out

vac_data = get_df(connect())
t = time_series(vac_data)

plots_vac["timeSeries"] = f'data:image/png;base64,{t}'
vac_data["prop"] = vac_data["cumseconds"] / pop
d = vac_data["date"][vac_data["prop"] > 0.5].iloc[-1]

#hypothesis test
date = datetime.date(2021, 4, 10)

A = vac_data[datetime.datetime.strptime(vac_data["date"],'%d/%m/%Y').date() < date]
B = vac_data[datetime.datetime.strptime(vac_data["date"],'%d/%m/%Y').date() > date]

nA = len(A)
nB = len(B)

den = np.sqrt(np.var(A["dailydeaths"])/nA + np.var(B["dailydeaths"])/nB)
t = (np.mean(A["dailydeaths"]) - np.mean(B["dailydeaths"])) / den

df = nA + nB - 2

T = stats.t.ppf(1-0.025, df)

#Plot for hypothesis test
def hyp_plot(df):
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
    out = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return out

h = hyp_plot(vac_data)
plots_vac["deaths"] = f'data:image/png;base64,{h}'

#outputs for app.py
data_vac["dateOfHalfVacc"] = datetime.datetime.strptime(d,'%d/%m/%Y').date()
data_vac["propVaccSoFar"] = round(max(vac_data["prop"]),2)

data_vac["dateOfSplit"] = date
data_vac["cumVacAtSplit"] = round(data_vac["prop"][data_vac["date"]==date],2)
data_vac["degreesOfFreedom"] = df
data_vac["t"] = t
data_vac["T"] = T