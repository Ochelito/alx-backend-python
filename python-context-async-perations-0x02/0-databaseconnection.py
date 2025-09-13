import sqlite3

class DatabaseConnection():

    """Initialize with database name"""
    def __init__(self, db_name="mydb.sqlite3"):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):

        """Open database connection when entering the with block"""
        print("Connecting to the database...")
        self.connection = sqlite3.connect(self.db_name)
        return self.connection # Return the connection object to be used in the with block

    def __exit__(self, exc_type, exc_value, traceback):

        """Close connection automatically when leaving the with block"""
        print("Closing the database connection...")
        if self.connection:
            self.connection.close()    
        return False # Propagate exceptions if any occurred. does not suppress exceptions

if __name__ == "__main__": 
    # Example usage    
    with DatabaseConnection("mydb.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)