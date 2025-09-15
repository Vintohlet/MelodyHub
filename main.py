import psycopg2
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')


conn_params = {
    "host": "",       
    "port": 5432,
    "dbname": "",       
    "user": "",        
    "password": "" 
}


queries = {
    "top_customers": """
        SELECT c.customer_id, c.first_name || ' ' || c.last_name AS full_name,
               ROUND(SUM(i.total), 2) AS revenue
        FROM customer c
        JOIN invoice i ON c.customer_id = i.customer_id
        GROUP BY c.customer_id, full_name
        ORDER BY revenue DESC
        LIMIT 5;
    """,

    "revenue_by_year": """
        SELECT EXTRACT(YEAR FROM i.invoice_date) AS year,
               ROUND(SUM(i.total), 2) AS revenue
        FROM invoice i
        GROUP BY year
        ORDER BY year;
    """,

    "avg_invoice_total": """
        SELECT ROUND(AVG(total), 2) AS avg_invoice,
               MIN(total) AS min_invoice,
               MAX(total) AS max_invoice
        FROM invoice;
    """,

    "tracks_per_album": """
        SELECT a.title AS album, COUNT(t.track_id) AS track_count
        FROM album a
        JOIN track t ON a.album_id = t.album_id
        GROUP BY a.title
        ORDER BY track_count DESC
        LIMIT 5;
    """
}

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
