import logging
import sqlite3

# Configure logging for the application
logging.basicConfig(filename='app.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define a class to interact with a SQLite database
class Database:
    # Initialize the class with a connection to the specified SQLite database file
    def __init__(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)  # Connect to the SQLite database
            self.cur = self.conn.cursor()  # Create a cursor object
            self.init_db()  # Initialize the database structure
        except sqlite3.Error as e:
            logging.error(f"Failed to connect to the database: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during database initialization: {e}")
            raise

    # Method to initialize the necessary tables in the database
    def init_db(self):
        try:
            # Execute SQL commands to create tables if they do not exist
            self.cur.execute("CREATE TABLE IF NOT EXISTS History (Question TEXT)")
            self.cur.execute("CREATE TABLE IF NOT EXISTS Credentials (Token TEXT, Org TEXT)")
            self.conn.commit()  # Commit the changes to the database
        except sqlite3.Error as e:
            logging.error(f"Failed to initialize database tables: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during database initialization: {e}")
            raise

    # Method to add a question to the database
    def add_question(self, Question):
        try:
            # Check if the question already exists
            self.cur.execute("SELECT Question FROM History WHERE question = ?", (Question,))
            if not self.cur.fetchone():
                # If the question does not exist, add it to the database
                self.cur.execute("INSERT INTO History(Question) VALUES(?)", (Question,))
                self.conn.commit()  # Commit the changes
        except sqlite3.Error as e:
            logging.error(f"Failed to add question: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in add_question: {e}")
            raise

    # Method to retrieve all questions from the database
    def get_questions(self):
        try:
            self.cur.execute("SELECT Question FROM History")
            return [item[0] for item in self.cur.fetchall()]  # Return a list of questions
        except sqlite3.Error as e:
            logging.error(f"Failed to retrieve questions: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in get_questions: {e}")
            raise

    # Method to delete a specific question from the database
    def delete_question(self, Question):
        try:
            self.cur.execute("DELETE FROM History WHERE Question = ?", (Question,))
            self.conn.commit()  # Commit the changes
        except sqlite3.Error as e:
            logging.error(f"Failed to delete question: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in delete_question: {e}")
            raise

    # Method to update or insert the API token in the database
    def set_api_token(self, Token):
        try:
            self.cur.execute("SELECT Token FROM Credentials")
            if self.cur.fetchone():
                # If a token already exists, update it
                self.cur.execute("UPDATE Credentials SET Token = ?", (Token,))
            else:
                # If no token exists, insert it
                self.cur.execute("INSERT INTO Credentials (Token) VALUES (?)", (Token,))
            self.conn.commit()  # Commit the changes
        except sqlite3.Error as e:
            logging.error(f"Failed to set API token: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in set_api_token: {e}")
            raise

    # Method to update or insert the API organization ID in the database
    def set_api_org(self, Org):
        try:
            self.cur.execute("SELECT Org FROM Credentials")
            if self.cur.fetchone():
                # If an organization ID already exists, update it
                self.cur.execute("UPDATE Credentials SET Org = ?", (Org,))
            else:
                # If no organization ID exists, insert it
                self.cur.execute("INSERT INTO Credentials (Org) VALUES (?)", (Org,))
            self.conn.commit()  # Commit the changes
        except sqlite3.Error as e:
            logging.error(f"Failed to set API organization: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in set_api_org: {e}")
            raise

    # Method to retrieve the API token from the database
    def get_api_token(self):
        try:
            self.cur.execute("SELECT Token FROM Credentials")
            result = self.cur.fetchone()
            return result[0] if result else None  # Return the token if it exists
        except sqlite3.Error as e:
            logging.error(f"Failed to retrieve API token: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in get_api_token: {e}")
            raise

    # Method to retrieve the API organization ID from the database
    def get_api_org(self):
        try:
            self.cur.execute("SELECT Org FROM Credentials")
            result = self.cur.fetchone()
            return result[0] if result else None  # Return the organization ID if it exists
        except sqlite3.Error as e:
            logging.error(f"Failed to retrieve API organization: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in get_api_org: {e}")
            raise

    # Method to delete the API token from the database
    def delete_api_token(self):
        try:
            self.cur.execute("DELETE FROM Credentials")  # Delete the token
            self.conn.commit()  # Commit the changes
        except sqlite3.Error as e:
            logging.error(f"Failed to delete API token: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in delete_api_token: {e}")
            raise

    # Method to delete the API organization ID from the database
    def delete_api_org(self):
        try:
            self.cur.execute("DELETE FROM Credentials")  # Delete the organization ID
            self.conn.commit()  # Commit the changes
        except sqlite3.Error as e:
            logging.error(f"Failed to delete API organization: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in delete_api_org: {e}")
            raise
