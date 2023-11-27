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
                        'AMENITIES': row[4],
                        'MAX_PEOPLE': row[2]
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
                        'AMENITIES': row[4],
                        'MAX_PEOPLE': row[2]
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

def checkUser(username,password):
    try:
        # Establish a connection
        connection = conn()

        if connection:
                    # Create a cursor from the connection
                    with connection.cursor() as cursor:
                        # Execute a SELECT query to check user credentials
                        query = "SELECT * FROM UsersWithPlainTextPassword WHERE username = ? AND password = ?"
                        cursor.execute(query, username, password)

                        # Fetch the result
                        user_data = cursor.fetchone()

                        if user_data:
                            # User exists and credentials are correct
                            return True
                        else:
                            # User does not exist or credentials are incorrect
                            return False
                        
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(f"Error executing the query. SQLState: {sqlstate}")
        return None
    
def bookAStayForGivenID(houseID):
    try:
        connection = conn()

        if connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM houses WHERE houseID = ?", (houseID,))
                house_data = cursor.fetchone()

                if house_data is not None:
                    return house_data
                else:
                    return None
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(f"Error executing the query. SQLState: {sqlstate}")
        return None  


def checkBookingWithGivenDateForHouse(houseId,date_from,date_to):
    try:
        connection = conn()
        if connection:
            with connection.cursor() as cursor:
                check_query = "SELECT COUNT(*) FROM HouseRental WHERE houseID = ? AND date_from <= ? AND date_to >= ?"
                cursor.execute(check_query, (houseId,date_from,date_to))
                count = cursor.fetchone()[0]
                if count == 0:
                    # If no booking exists, insert the values
                    insert_query = "INSERT INTO HouseRental (houseID, date_from, date_to) VALUES (?, ?, ?)"
                    cursor.execute(insert_query, (houseId, date_from, date_to))
                    return True
                else:
                    return False
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(f"Error executing the query. SQLState: {sqlstate}")
    finally:
        if connection:
            connection.close()