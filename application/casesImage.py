from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

save_to = '/application/static/images'

clouddb = 'cockroachdb://Arjun:ZTP0gR_dTDFPapT53EySTw@chief-wallaby-3959.6zw.cockroachlabs.cloud:26257/covid19-project?sslmode=verify-full'

try:
    engine = create_engine(clouddb)

    query = 'SELECT date, dailycases FROM cases;'
    cases = pd.read_sql_query(query,engine)
    cases = cases.fillna(0)

    plt.plot(cases["date"],cases["dailycases"],color='purple')
    plt.title("COVID-19 cases in England")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    plt.xticks(cases["date"][list(range(0,len(cases),int(round(len(cases)/5,0))))])
    plt.savefig(save_to + 'cases.png')
except:
    cases = "failed to connect to db"