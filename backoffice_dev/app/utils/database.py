import pyodbc
from app.config import get_connection

class DatabaseInterface:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseInterface, cls).__new__(cls)
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

    def getcountfromquery(self, query: str) -> int:
        """
        Executes a SELECT COUNT(*) query based on the provided query and returns the count.

        Args:
            query (str): The original SELECT SQL query.

        Returns:
            int: The count of rows that the original query would return.
                 Returns 0 if the count is zero, no results are found for the count,
                 or if an error occurs during the query.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            if conn is None:
                print("Error: Could not establish database connection.")
                return 0

            cursor = conn.cursor()
            count_query = f"SELECT COUNT(*) FROM ({query}) AS subquery_for_count"
            
            cursor.execute(count_query)
            result_row = cursor.fetchone()
            
            if result_row and result_row[0] is not None:
                return int(result_row[0])
            else:
                return 0

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Database query error: {sqlstate}")
            print(ex)
            return 0
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def update(self, table:str,values:dict,where:str):
        """
        Executes an UPDATE query against SQL Server.

        Args:
            table (str): The name of the table to update.
            values (dict): A dictionary of column-value pairs to update.
            where (str): The WHERE clause to specify which rows to update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            if conn is None:
                print("Error: Could not establish database connection.")
                return False

            cursor = conn.cursor()
            set_clause = ', '.join([f"{key} = ?" for key in values.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE 1=1 "

            if where and where.strip():
                query += f" AND {where}"

            params = list(values.values())
            
            cursor.execute(query, params)
            conn.commit()
            return True

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Database update error: {sqlstate}")
            print(ex)
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()       


if __name__ == '__main__':
    pass
    