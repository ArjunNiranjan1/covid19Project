from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

base = os.getcwd()
cert = base + '/root.crt'
user = os.getenv('DB_USER')
pw = os.getenv("DB_PASSWORD")

#Connect to db
def connect():
    clouddb = f'cockroachdb://{user}:{pw}@chief-wallaby-3959.6zw.cockroachlabs.cloud:26257/covid19-project?sslmode=verify-ca&sslrootcert={cert}'
    engine = create_engine(clouddb)
    return engine

#Query date, daily cases, daily deaths
def query(engine):
    q = 'SELECT cases.date, cases.dailycases, deaths.dailydeaths FROM cases INNER JOIN deaths ON cases.date=deaths.date;'
    df = pd.read_sql_query(q, engine)
    return df

#Generate plots

