# db_operations.py
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='root',
            user='RootUser',
            password='Gitkoding2024$',
            database='library_db'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def execute_query(query, data=None):
    """Execute a single query."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            connection.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

def fetch_query(query, data=None):
    """Fetch data from the database."""
    connection = create_connection()
    result = None
    if connection:
        cursor = connection.cursor()
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
    return result
