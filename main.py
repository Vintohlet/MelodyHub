import psycopg2
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn_params = {
    "host": "",       
    "port": "",
    "dbname": "",       
    "user": "postgres",        
    "password": "" 
}

# File for SQL Queries
SQL_FILE = "" 


def load_queries_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    queries = [q.strip() for q in sql_content.split(";") if q.strip()]
    return {f"query_{i+1}": q for i, q in enumerate(queries)}


queries = load_queries_from_file(SQL_FILE)

def run_queries():
    conn = psycopg2.connect(**conn_params)

    for name, query in queries.items():
        print(f"\n--- {name.upper()} ---")
        df = pd.read_sql_query(query, conn)
        print(df)

        df.to_csv(f"{name}.csv", index=False)

    conn.close()

if __name__ == "__main__":
    run_queries()
