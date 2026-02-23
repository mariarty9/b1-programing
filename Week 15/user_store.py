import json
import sqlite3

class UserStore:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()                          # Initialize the database; create table if it doesn't exist

    def init_db(self):                          # Creates users table if it doesn't exist
        conn = None                             # Starts as nothing/empty
        try:
            conn = sqlite3.connect(self.db_path)    # Connect to the SQlite database; if the db file doesn't exist, SQL creates it automatically
            cursor = conn.cursor()              # Cursor is lika a pointer that lets us execute SQL commands
            # CREATE TABLE statement in SQL; triple quotes allow us to write multi-line strings
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            ''')
            conn.commit()                       # Saves changes to the database file; without it the able wouldn't be created
            print("Database initialized successfully (user table created)")
        except Exception as e:
            print(f"Error initializing database: {e}")      # If any error occurs, jump to the error block

        finally:                                # Runs no matter what; but here I wanted to check if we actually create a connection
            if conn:                            # If conn is not None then that means sqlite3.conncet() succeeded
                conn.close()                    # Close the database connection


    def load(self):                             # Returns list of user dictionaries from database
        conn = None
        users = []
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row      # Special setting that allows to access columns by name; without this, we would get tulpes like (1, "Name", "Email"); with this row['id'], row['name']...
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users ORDER BY id")     # Retrieve data from columns (id, name, email) from the users table sort by ID
            rows = cursor.fetchall()            # Fetch all rows from the result and return the list of Row objects
            for row in rows:
                user = {                        # Create a dictionary for this user
                    'id': row['id'],
                    'name': row['name'],
                    'email': row['email']
                }
                users.append(user)              # Add this user dictionary to the list
            print(f"Loaded {len(users)} users from database")
            return users
        except Exception as e:
            print(f"Error loading users:{e}")
            return []                           # Retunrs empty list  is the error occurs
        finally:
            if conn:                            # Always close connection
                conn.close()


    def save(self, users):                      # Inserts or updates users in the database
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users") # Remove every row form the users table, because we are replacing all data
            for user in users:
                cursor.execute(
                    "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",         # Questionmarks are placeholders for actual values
                    (user['id'], user['name'], user['email'])
                )
            
            conn.commit()
            print(f"Saved {len(users)} users to databse")
            return True                         # To indicate success

        except Exception as e:
            print(f"Error saving users: {e}")
            return False                        # To indicate failure
        finally:
            if conn:
                conn.close() 


    def find_by_id(self, user_id):              # Returns user dict or None using SQL query
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row      # Enable column access by name
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, name, email FROM users WHERE id = ?",
                (user_id,)                         # The comma makes it tulpe
            )
            row = cursor.fetchone()                # Fetch one row 
            if row:                                # Check if we found a row
                user = {
                    'id': row['id'],
                    'name': row['name'],
                    'email': row['email']
                }                    
                print(f"Found user with ID {user_id}")
                return user
            print(f"User with ID {user_id} not found")
            return None
        
        except Exception as e:
            print(f"Error finding user: {e}")
            return None
        finally:
            if conn:
                conn.close()


    def create_user(self, user_data):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute( 
                "INSERT INTO users (name, email) VALUES (?, ?)",    # Insert new user; we don't specify the ID because the db generates it automatically; the ? placeholders will be filled with name and email
                (user_data['name'], user_data['email'])
            )
            conn.commit()

            user_id = cursor.lastrowid                              # Get the auto-generated ID of the new user; lastrowid is a property that contains the ID of the last inserted row
            print(f"Created new user with ID {user_id}")           
            return self.find_by_id(user_id)
        
        except sqlite3.IntegrityError as e:                         # Error that occurs when a UNIQUE constraint is violated; here it means using email that already exists
            if "UNIQUE constraint failed" in str(e):                # Check if the error message mentions UNIQUE constraint
                print(f"Email {user_data['email']} already exists") 
                return None
            print(f"Integrity error: {e}")                          # If other integrity error occurs
            return None
        finally:
            if conn:
                conn.close()

    def update_user(self, user_id, user_data):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(                                     # Check if the email is already used by a different user; this excludes the current user (because of previous test)
                "SELECT id FROM users WHERE id = ? AND id != ?", (user_data['email'], user_id)
            )
            if cursor.fetchone():                           
                print(f"Email {user_data['email']} already in use by another user")
                return None                                     # Email exists for different user
            cursor.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",        # MOdify existing data
                (user_data['name'], user_data['email'], user_id)
            )

            conn.commit()
        
            if cursor.rowcount > 0:                                         # Check if the error message mentions UNIQUE constraint; Check if any row was actually updated
                print(f"Updated user with ID {user_id}")                    
                return self.find_by_id(user_id)                             # Return the updated user by calling find_by_id
            return None
        except sqlite3.IntegrityError as e:
            print(f"Integrity error: {e}")
            return None
        except Exception as e:
            print(f"Error updating user: {e}")
            return None
        finally:
            if conn:
                conn.close()


    def delete_user(self, user_id):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM users WHERE id = ?", (user_id,)
            )
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Deleted user with ID {user_id}")
                return True
            else:
                print(f"User with ID {user_id} not found for deletion")
                return False
        except Exception as e:
            print(f"Erro deleting user: {e}")
            return False
        finally:
            if conn:
                conn.close()

    