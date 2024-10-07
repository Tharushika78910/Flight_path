from turtledemo.sorting_animate import start_ssort

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='flight_path',
    user='root',
    password='12345',
    autocommit=True
)

#FUNCTIONS

#SELECT 30 AIRPORTS FOR THE GAME
def get_airports():
    sql = """SELECT iso_country, ident, name, type, latitude_deg, longitude_deg
FROM airport
WHERE continent = 'EU' 
AND type='large_airport'
ORDER by name asc
LIMIT 30;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

print("Welcome to Flight Path!")