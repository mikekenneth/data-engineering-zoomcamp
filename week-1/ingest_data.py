import os
import argparse
import pandas as pd
from sqlalchemy import create_engine


def main(params):
    filename = "output.parquet"
    try:
        engine = create_engine(f"postgresql://{params.user}:{params.password}@{params.host}:{params.port}/{params.db}")
        engine.connect()
    except:
        print("Wrong Database parameters")

    # Download File
    os.system("mkdir -p data/")
    # os.system(f"wget {params.url} -O data/{filename}")

    df = pd.read_parquet(f"data/{filename}")

    # Load all data into Postgresql Table
    df.to_sql(name=params.table_name, con=engine, if_exists="replace")
    print(f"Loaded data into {params.table_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", type=int, help="port for postgres")
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument("--table_name", help="table name where we store the data")
    parser.add_argument("--url", help="url of the csv file")

    args = parser.parse_args()

    main(args)
