"""
Database manager for handling all database operations.
"""
import sqlite3
from typing import List, Dict, Any, Optional
from config import DATABASE_PATH


class DatabaseManager:
    """Manages database connections and operations."""

    def __init__(self):
        self.db_path = str(DATABASE_PATH)

    def get_connection(self):
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results as list of dictionaries.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            List of dictionaries representing rows
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()

            # Convert Row objects to dictionaries
            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def execute_write(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Last row ID for INSERT, or number of affected rows
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            last_row_id = cursor.lastrowid
            affected_rows = cursor.rowcount

            conn.close()

            return last_row_id if last_row_id > 0 else affected_rows

        except Exception as e:
            print(f"Error executing write operation: {e}")
            raise

    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Execute multiple write operations.

        Args:
            query: SQL query string
            params_list: List of parameter tuples

        Returns:
            Number of affected rows
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()

            affected_rows = cursor.rowcount
            conn.close()

            return affected_rows

        except Exception as e:
            print(f"Error executing batch operation: {e}")
            raise

    def execute_transaction(self, operations: List[Dict[str, Any]]) -> bool:
        """
        Execute multiple operations in a transaction.

        Args:
            operations: List of dicts with 'query' and 'params' keys

        Returns:
            True if successful, False otherwise
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            for operation in operations:
                query = operation.get('query')
                params = operation.get('params', ())
                cursor.execute(query, params)

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            print(f"Error executing transaction: {e}")
            return False

    def get_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """
        Execute a query and return a single row.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Dictionary representing the row, or None if not found
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            conn.close()

            return dict(row) if row else None

        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        query = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
        """
        result = self.execute_query(query, (table_name,))
        return len(result) > 0

    def get_table_count(self, table_name: str) -> int:
        """Get the number of rows in a table."""
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.get_one(query)
        return result['count'] if result else 0


# Create a global instance
db = DatabaseManager()
