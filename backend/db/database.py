import psycopg2
import os

class Database:
    def __init__(self):
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.db = os.getenv('POSTGRES_DB')
        self.host = 'db'  # Assuming the database is running in a Docker container named 'db'
        self.port = 5432  # Default PostgreSQL port
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                database=self.db,
                host=self.host,
                port=self.port
                )
            print("Database connection successful")
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def execute_query(self, query, params=None):
        try:
            if not self.conn:
                self.connect()
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                self.conn.commit()
                return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            return None

    def fetch_one(self, query, params=None):
        try:
            if not self.conn:
                self.connect()
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchone()
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            return None

    def get_by_id(self, table_name, id):
        query = f"SELECT * FROM {table_name} WHERE id = %s"
        result = self.fetch_one(query, (id,))
        return result

    def get_by_ids(self, table_name, ids):
        query = f"SELECT * FROM {table_name} WHERE id IN %s"
        result = self.execute_query(query, (tuple(ids),))
        return result

    def delete_data(self, table_name, where_condition):
        if not where_condition:
            print("Error: WHERE condition is required for delete operation")
            return None
        query = f"DELETE FROM {table_name} WHERE {where_condition}"
        result = self.execute_query(query)
        return result

    def update_data(self, table_name, id, data):
        set_values = ", ".join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table_name} SET {set_values} WHERE id = %s"
        params = list(data.values()) + [id]
        result = self.execute_query(query, params)
        return result
