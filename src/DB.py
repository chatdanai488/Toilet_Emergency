import pyodbc

class DB:
    def __init__ (self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-HDSHPKBA\\TOILET_EMERGENCY;'
            'DATABASE=dbo;'
            'UID=TOILETMASTER;'
            'PWD=POOP123;'
        )

    
    def Fetch(self):
        # Create a cursor
        with self.connection.cursor() as cursor:
            # Execute a SQL query
            cursor.execute("SELECT * FROM dbo.LocTb")

            # Fetch results
            rows = cursor.fetchall()

            # Process results
            for row in rows:
                print(row)

        
    
    def Insert(self):
        
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO dbo.LocTb (fDate, fStdId, fLat, fLong, fAlt, fImg, fPlace, fStat) VALUES ('2024-03-04', 'ABC12345', 40.7128, -74.0060, 10.0, 'image.jpg', 'New York', '1');")

            

    

if __name__ == "__main__":
    Database = DB()
    Database.Fetch()
    Database.Insert()