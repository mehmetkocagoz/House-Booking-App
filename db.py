import pyodbc
from dotenv import load_dotenv
import os
load_dotenv()

server = 'flaskdatabasemdtrm.database.windows.net'
port = 1433
user = 'midtermdatabase'
password = os.getenv("AZURE_PASSWORD")
database = 'flaskappdatabase'

# Build connection string
conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server},{port};DATABASE={database};UID={user};PWD={password}"
def conn():
    try:
        # Create a connection
        with pyodbc.connect(conn_str, timeout=5) as conn:
            return conn

    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(sqlstate)
        return f"Error connecting to the database. SQLState: {sqlstate}"

def getHouses():
    try:
        # Establish a connection
        connection = conn()

        # Check if the connection is successful
        if connection:
            # Create a cursor from the connection
            with connection.cursor() as cursor:
                # Execute a SELECT query
                cursor.execute("SELECT * FROM houses")

                # Fetch all the rows
                rows = cursor.fetchall()
                houses_data_list = []
                for row in rows:
                    house_entry = {
                        'ID': row[0],
                        'CITY': row[1],
                        'DESCRIPTION': row[3],
                        'AMENETIES': row[4],
                        'MAX_PEOPLE': row[2],
                        'ISBOOKED': row[5]
                    }
                    houses_data_list.append(house_entry)


            return houses_data_list

    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(f"Error executing the query. SQLState: {sqlstate}")
        return None
    finally:
        # Close the connection
        connection.close()


def getHousesWithCity(city):
    try:
        # Establish a connection
        connection = conn()

        # Check if the connection is successful
        if connection:
            # Create a cursor from the connection
            with connection.cursor() as cursor:
                # Execute a SELECT query with a WHERE clause for the specified city
                cursor.execute("SELECT * FROM houses WHERE CITY = ?", (city,))

                # Fetch all the rows
                rows = cursor.fetchall()
                houses_data_list = []
                for row in rows:
                    house_entry = {
                        'ID': row[0],
                        'CITY': row[1],
                        'DESCRIPTION': row[3],
                        'AMENITIES': row[4],  # Corrected typo: 'AMENETIES' to 'AMENITIES'
                        'MAX_PEOPLE': row[2],
                        'IS_BOOKED': row[5]  # Adjusted to 'IS_BOOKED'
                    }
                    houses_data_list.append(house_entry)

            return houses_data_list

    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(f"Error executing the query. SQLState: {sqlstate}")
        return None
    finally:
        # Close the connection
        if connection:
            connection.close()
