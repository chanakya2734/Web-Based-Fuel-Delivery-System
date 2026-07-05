import sqlite3
import mysql.connector

class DBConnection:
    def __init__(self, is_sqlite, conn):
        self.is_sqlite = is_sqlite
        self.conn = conn
        if is_sqlite:
            self.conn.row_factory = sqlite3.Row

    def cursor(self, dictionary=False):
        raw_cursor = self.conn.cursor()
        return DBCursor(self.is_sqlite, raw_cursor, dictionary)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

class DBCursor:
    def __init__(self, is_sqlite, cursor, dictionary):
        self.is_sqlite = is_sqlite
        self.cursor = cursor
        self.dictionary = dictionary

    def execute(self, sql, params=None):
        if self.is_sqlite:
            sql = sql.replace("%s", "?")
            
        if params is not None:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)

    def fetchall(self):
        results = self.cursor.fetchall()
        if self.is_sqlite and self.dictionary:
            return [dict(row) for row in results]
        return results

    def fetchone(self):
        result = self.cursor.fetchone()
        if self.is_sqlite and self.dictionary and result:
            return dict(result)
        return result

    def close(self):
        self.cursor.close()

def setup_sqlite_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manager (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS delivery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fuelAmount TEXT,
        fuelType TEXT,
        userLocationLat REAL,
        userLocationLng REAL,
        petrolBunkLocationLat REAL,
        petrolBunkLocationLng REAL,
        timestamp_booked TEXT,
        timestamp_delivered TEXT,
        status TEXT DEFAULT 'Pending',
        delivered TEXT DEFAULT 'Not Delivered'
    )
    """)
    cursor.execute("INSERT OR IGNORE INTO manager (username, password) VALUES ('admin', 'admin123')")
    cursor.execute("INSERT OR IGNORE INTO customer (username, password) VALUES ('customer1', 'cust123')")
    cursor.execute("INSERT OR IGNORE INTO delivery (username, password) VALUES ('delivery1', 'del123')")
    conn.commit()
    cursor.close()

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fuel"
        )
        print("Connected to MySQL successfully!")
        return DBConnection(False, conn)
    except mysql.connector.Error as e:
        print(f"MySQL connection failed: {e}. Falling back to SQLite...")
        conn = sqlite3.connect("fuel.db")
        setup_sqlite_db(conn)
        return DBConnection(True, conn)

try:
    mydb = get_db_connection()
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT * FROM customer WHERE username = %s AND password = %s",
        ('customer1', 'cust123')
    )
    myresult = mycursor.fetchall()
    print("Login lookup result:", myresult)
    print("Login successful:", len(myresult) > 0)
    mycursor.close()
    mydb.close()
except Exception as e:
    import traceback
    traceback.print_exc()
