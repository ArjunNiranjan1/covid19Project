from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os

save_to = '/app/application/static/images'

load_dotenv()


user = os.getenv('DB_USER')
pw = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_DATABASE')



def read():
    clouddb = f'cockroachdb://{user}:{pw}@{host}:{port}/{database}?sslmode=verify-ca&sslrootcert=app/application/root.crt'
    engine = create_engine(clouddb)
    query = 'SELECT date, dailycases FROM cases;'
    cases = pd.read_sql_query(query,engine)
    cases = cases.fillna(0)
    return cases

def plot(cases):
    sns.set_theme()

    plt.plot(cases["date"],cases["dailycases"],color='purple')
    plt.title("COVID-19 cases in England")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    plt.xticks(cases["date"][list(range(0,len(cases),int(round(len(cases)/5,0))))])
    plt.savefig(save_to + 'cases.png')
