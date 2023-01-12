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

#hypothesis test
vac_data["prop"] = vac_data["cumseconds"] / pop
d = vac_data["date"][vac_data["prop"] > 0.5].iloc[-1]
data_vac["dateOfHalfVacc"] = datetime.datetime.strptime(d,'%d/%m/%Y').date()
data_vac["propVaccSoFar"] = round(max(vac_data["cumseconds"]) / pop,2)

setA = vac_data[vac_data["date"] < d]
setB = vac_data[vac_data["date"] > d]

mA = round(np.mean(setA["dailydeaths"]),2)
mB = round(np.mean(setB["dailydeaths"]),2)
nA = len(setA)
nB = len(setB)
sA = round(np.sqrt(np.var(setA["dailydeaths"])),2)
sB = round(np.sqrt(np.var(setB["dailydeaths"])),2)

mDiff = mA - mB
sP = ((nA -1)*sA**2 + (nB -1)*sB**2) / (nA + nB - 2)
t = mDiff / (sP * np.sqrt(nA**-1 + nB**-1))
#regression

#outputs for app.py
data_vac["dateOfHalfVacc"] = datetime.datetime.strptime(d,'%d/%m/%Y').date()
data_vac["propVaccSoFar"] = round(max(vac_data["cumseconds"]) / pop,2)
data_vac["test"] = [t, sP]