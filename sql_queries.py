# SQL statement to create a new table named 'books' if it does not already exist.
CREATE_TABLE = """
                CREATE TABLE IF NOT EXISTS books (
                            ID      INTEGER PRIMARY KEY,
                            Title   VARCHAR,
                            Author  VARCHAR,
                            Rating  FLOAT,
                            ISBN    VARCHAR
                        )
               """

# SQL statement to delete all records from the 'books' table.
TRUNCATE_TABLE = """DELETE FROM books"""

# SQL statement to select all records from the 'books' table. This query...
# ...retrieves every column for all rows.
VIEW_RECORDS = """SELECT * FROM books"""

# SQL statement to insert a new record into the 'books' table. This statement ...
# ...uses placeholders (?, ?, ?, ?) for parameter substitution. NULL is used for...
# ...the ID column to utilize SQLite's auto-increment functionality.
INSERT_RECORD = """
                    INSERT INTO books
                    VALUES(NULL, ?, ?, ?, ?)
                """

# SQL statement to delete a specific record from the 'books' table based on the ID.
# A placeholder (?) for ID is used to safely delete the specified record.
DELETE_RECORD = """
                    DELETE FROM books
                    WHERE ID = ?
                 """

# SQL statement to update a specific record in the 'books' table by ID. It uses...
# ...placeholders for each field to ensure safe data handling.
UPDATE_RECORD = """
                    UPDATE books
                    SET Title = ?, Author = ?,
                        Rating = ?, ISBN = ?
                    WHERE ID = ?
                 """
