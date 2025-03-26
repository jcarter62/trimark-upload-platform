from decouple import config
import pyodbc
"""
data_writer.py - Writes data to a SQL Server database.

Usage:
    from data_writer import write_to_db

Arguments:
    data: The data to write to the database.

Description:
    This script contains functions for writing data to a SQL Server database.
    It uses the pyodbc library to connect to the database and execute SQL queries.
"""


# ref: https://chat.openai.com/share/cd81b52d-b14c-4c71-9934-a922eac5081e
#
class DataWriter:

    def __init__(self, dataobj):
        self.server = config('DB_SERVER')
        self.database = config('DB_NAME')
        self.instance = config('DB_INSTANCE')
        self.records = dataobj["data"]
        return


    def execute(self):
        self.connect()
        self.insert_records()
        self.close()


    def connect(self):
        connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={self.server}\\{self.instance};Database={self.database};Trusted_Connection=yes"
        self.conn = pyodbc.connect(connection_string)

    def is_bad_record(self, record):
        # Check if the record is valid
        if record["Site Name"] is None or record["Site Name"] == "" or \
                record["Member"] is None or record["Member"] == "" or \
                record["Locations"] is None or record["Locations"] == "" :
            return True
        return False

    def insert_records(self):
        if self.conn is None:
            print("Please connect to the database first.")
            return

        irec = 0
        cursor = self.conn.cursor()

        # Assuming the table "trimark" has columns "col1", "col2", "col3"
        insert_query = ('''
                INSERT INTO Trimark 
                   (Member,Locations,SiteName,Meters,ExternalID
                   ,Latitude,Longitude,Location,City,State,ZipCode
                   ,DeviceType,SerialNumber,BadgeNumber,FormType,Class
                   ,Constant,InstallDate,LastInterrogation,MeterReadingDate
                   ,MeterReadingValue,PeakDemandDate,PeakDemandValue) 
                Values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''' )

        try:
            irec = 0
            inserted = 0
            for record in self.records:
                try:
                    irec += 1
                    if self.is_bad_record(record):
                        print(f"Bad record at {irec}")
                        continue

                    badge_number = record["Badge Number"]
                    serial_number = record["Serial Number"]
                    value = record["Meter Reading Value"]
                    rdate = record["Meter Reading Date"]

                    params = (record["Member"], record["Locations"], record["Site Name"], record["Meters"],
                              record["External ID"], record["Latitude"], record["Longitude"], record["Location"][:90],
                              record["City"], record["State"],
                              record["Zip"], record["Device Type"], record["Serial Number"], record["Badge Number"],
                              record["Form Type"], record["Class"], record["Constant"], record["Install Date"],
                              record["Last Interval"], record["Meter Reading Date"], record["Meter Reading Value"],
                              record["Peak Demand Date"], record["Peak Demand Value"])

                    # determine if the record already exists
                    # check for duplicates
                    check_query = "SELECT COUNT(*) FROM Trimark WHERE SerialNumber = ? AND BadgeNumber = ? AND MeterReadingDate = ?"
                    cursor.execute(check_query, (serial_number, badge_number, rdate))
                    count = cursor.fetchone()[0]
                    if count > 0:
                        # print(f"Record already exists for Badge:{badge_number}, SN:{serial_number} and Meter Reading Date: {rdate}")
                        skip = True
                    else:
                        skip = False
                    if not skip:
                        cursor.execute(insert_query, params)
                        print(f'INS:Badge:{badge_number}/SN:{serial_number}/DT:{rdate}/Val:{value}/{irec}')
                        inserted += 1
                    else:
                        print(f'SKIP:Badge:{badge_number}/SN:{serial_number}/DT:{rdate}/Val:{value}/{irec}')
                except Exception as e:
                    print(f"ERR:row:{irec}/{e}")

            if inserted > 0:
                print(f"Inserted {inserted} records into the database.")
                self.conn.commit()
        except Exception as e:
            print(f"An error occurred at record {irec}: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

