import pyodbc
from app.config import get_connection

class db:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(db, cls).__new__(cls)
        return cls._instance
    

    def getallfromquery(self, query: str):
        """
        Executes a SELECT query against SQL Server and returns a list of dictionaries.

        Args:
            query (str): The SELECT SQL query to execute.

        Returns:
            list: A list of dictionaries, where each dictionary represents a row,
                  with keys as column names.
            None: If no results are found or if an error occurs during the query.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            if conn is None:
                print("Error: Could not establish database connection.")
                return None

            cursor = conn.cursor()
            cursor.execute(query)
            
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results if results else None

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Database query error: {sqlstate}")
            print(ex)
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


if __name__ == '__main__':
    pass
    