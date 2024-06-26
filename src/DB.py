import pyodbc
import datetime


class DB:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-BDV70FFI\\SQLSERVER2022;'
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
            cursor.execute(
                "INSERT INTO dbo.LocTb (fDate, fStdId, fLat, fLong, fAlt, fImg, fPlace, fStat) VALUES ('2024-03-04', 'ABC12345', 40.7128, -74.0060, 10.0, 'image.jpg', 'New York', '1');")

    def Insert_Floor(self, Data):
        data = Data
        print(data[4])
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO dbo.FloorTb (MapId, MapName, DateCrt, DateChg, PicPath) VALUES (?, ?, ?, ?, ?);"
            cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4]))
            cursor.commit()

    def Fetch_Floor(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT MapId, MapName, DateCrt, DateChg, PicPath FROM dbo.FloorTb"
            cursor.execute(sql)

            rows = cursor.fetchall()
            data_array = []
            for row in rows:
                data_array.append(list(row))

            for sublist in data_array:
                for i, item in enumerate(sublist):
                    if isinstance(item, datetime.datetime):
                        sublist[i] = item.strftime("%Y/%m/%d %H:%M:%S")

            cursor.commit()
            return data_array

    def Delete_Floor(self, value):
        print(value)
        with self.connection.cursor() as cursor:
            # Replace <column_name> with the actual column name
            sql = "DELETE FROM dbo.FloorTb WHERE MapId = ?"
            cursor.execute(sql, (value,))
            cursor.commit()

    def Edit_Floor(self, Data):
        data = Data
        with self.connection.cursor() as cursor:
            sql = "UPDATE dbo.FloorTb SET MapId = ?, MapName = ?, DateChg = ?, PicPath = ? WHERE Picpath = ?"
            cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4]))
            cursor.commit()

    def Insert_Map(self, Data):
        data = Data
        with self.connection.cursor() as cursor:
            if data[6] == "dot":
                x, y = data[5][0], data[5][1]
                sql = "INSERT INTO dbo.FloorMapTb (fDate, fMapId, fMapName, fMapIp, fMapRmrk, fCoordsX1,fCoordsY1,fMapMode, fImg, fColor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
                cursor.execute(
                    sql, (data[0], data[1], data[2], data[3], data[4], x, y, data[6], data[7], data[8]))
                cursor.commit()
            else:
                x, y = data[5][0][0], data[5][0][1]
                x1, y1 = data[5][1][0], data[5][1][1]
                sql = "INSERT INTO dbo.FloorMapTb (fDate, fMapId, fMapName, fMapIp, fMapRmrk, fCoordsX1,fCoordsY1,fCoordsX2,fCoordsY2,fMapMode, fImg, fColor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
                cursor.execute(sql, (data[0], data[1], data[2], data[3],
                               data[4], x, y, x1, y1, data[6], data[7], data[8]))
                cursor.commit()

    def Fetch_Map(self, map_path):
        with self.connection.cursor() as cursor:
            sql = "SELECT fDate, fMapId, fMapName, fMapIp, fMapRmrk, fCoordsX1,fCoordsY1,fCoordsX2,fCoordsY2,fMapMode, fImg, fColor FROM dbo.FloorMapTb WHERE fImg = ?"
            cursor.execute(sql, (map_path))

            rows = cursor.fetchall()
            data_array = []
            for row in rows:
                data_array.append(list(row))

            cursor.commit()
            return data_array

    def Update_Map(self, Data):
        data = Data
        with self.connection.cursor() as cursor:
            if data[6] == "dot":
                x, y = data[5][0], data[5][1]
                sql = "UPDATE dbo.FloorMapTb SET fDate = ?, fMapId = ?, fMapName = ?, fMapIp = ?, fMapRmrk = ?, fCoordsX1 = ?,fCoordsY1 = ?,fMapMode = ?, fImg = ?, fColor = ?, WHERE fmapId = ? "
                cursor.execute(sql, (data[0], data[1], data[2], data[3],
                               data[4], x, y, data[6], data[7], data[8], data[9]))
                cursor.commit()
            else:
                x, y = data[5][0][0], data[5][0][1]
                x1, y1 = data[5][1][0], data[5][1][1]
                sql = "UPDATE dbo.FloorMapTb SET fDate = ?, fMapId = ?, fMapName = ?, fMapIp = ?, fMapRmrk = ?, fCoordsX1 = ?,fCoordsY1 = ?,fCoordsX2 = ?,fCoordsY2 = ?,fMapMode = ?, fImg = ?, fColor = ? WHERE fmapId = ?"
                cursor.execute(sql, (data[0], data[1], data[2], data[3],
                               data[4], x, y, x1, y1, data[6], data[7], data[8], data[9]))
                cursor.commit()

    def Delete_Map(self, Data1, Data2):
        with self.connection.cursor() as cursor:
            # Replace <column_name> with the actual column name
            sql = "DELETE FROM dbo.FloorMapTb WHERE fMapId = ? AND fMapName = ?"
            cursor.execute(sql, (Data1, Data2))
            cursor.commit()

    def Fetch_Indi_Map(self, Data):
        with self.connection.cursor() as cursor:
            sql = "SELECT fDate, fMapId, fMapName, fMapIp, fMapRmrk, fCoordsX1,fCoordsY1,fCoordsX2,fCoordsY2,fMapMode, fImg, fColor FROM dbo.FloorMapTb WHERE fMapName = ?"
            cursor.execute(sql, (Data))

            rows = cursor.fetchall()
            data_array = []
            for row in rows:
                data_array.append(list(row))

            cursor.commit()
            return data_array

    def Insert_Alert(self, Data):
        data = Data
        with self.connection.cursor() as cursor:
            sql = """INSERT INTO Alerts (fAlertDate, fAlertLoc, fAlertId, fAlertStatus)
            VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, (data[0], data[1], data[2], data[3]))
            cursor.commit()

    def Fetch_Pending(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT fAlertLoc, fAlertId FROM dbo.Alerts WHERE fAlertStatus = 1"
            cursor.execute(sql)

            rows = cursor.fetchall()
            data_array = []
            for row in rows:
                data_array.append(list(row))

            cursor.commit()
            return data_array

    def Fetch_Alert_Log(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT TOP 50 fAlertDate, fAlertLoc, fAlertId,fAlertStatus FROM dbo.Alerts ORDER BY fAlertDate DESC"
            cursor.execute(sql)

            rows = cursor.fetchall()
            data_array = []
            for row in rows:
                data_array.append(list(row))

            cursor.commit()
            return data_array

    def Fetch_Pending_Map(self, Data):
        with self.connection.cursor() as cursor:
            sql = "SELECT fDate, fMapId, fMapName, fMapIp, fMapRmrk, fCoordsX1,fCoordsY1,fCoordsX2,fCoordsY2,fMapMode, fImg, fColor FROM dbo.FloorMapTb WHERE fMapName = ?"
            cursor.execute(sql, Data)

            rows = cursor.fetchall()
            data_array = []
            for row in rows:
                data_array.append(list(row))

            cursor.commit()
            return data_array

    def Update_Emergency_Status(self, data):
        with self.connection.cursor() as cursor:
            sql = "UPDATE dbo.Alerts SET fAlertStatus = 0 WHERE fAlertLoc = ? AND fAlertId = ?"
            cursor.execute(sql, (data[0], data[1]))
            cursor.commit()

    def Active_Emergency_Check(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT fAlertLoc FROM dbo.Alerts WHERE fAlertStatus = 1"
            cursor.execute(sql)

            rows = cursor.fetchall()
            data_array = []
            for row in rows:
                data_array.append(list(row))

            cursor.commit()
            return data_array


if __name__ == "__main__":
    Database = DB()
    Database.Fetch_Floor()
