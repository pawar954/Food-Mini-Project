#Step 2 — Test the connection main.py    

from database import get_connection #

def main():
    connection = get_connection() # This represents the connection/session between your Python application and SQLite.
    print("Database connection successful.")
    connection.close()

if __name__ == "__main__":
    main()