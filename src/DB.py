import pyodbc

class DB:
    def __init__ (self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-HDSHPKBA\TOILET_EMERGENCY;'
            'DATABASE=dbo;'
            'UID=TOILETMASTER;'
            'PWD=POOP123;'
        )
    
    def Fetch(self):
        # Create a cursor
        cursor = self.connection.cursor()

        # Execute a SQL query
        cursor.execute("SELECT * FROM table_name")

        # Fetch results
        rows = cursor.fetchall()

        # Process results
        for row in rows:
            print(row)

        # Close the cursor and connection
        cursor.close()
        self.connection.close()
    
if __name__ == "__main__":
    Database = DB()
    Database.Fetch()
    