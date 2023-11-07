
# Import the Application class from the gui.app module
from gui.app import Application
# Import the logging module for tracking events that occur while the software runs
import logging

def main():
    # Set up logging and Configure it to write messages to a file 'app.log'
    logging.basicConfig(filename='app.log',
                        level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    try:
        # Create an instance of the Application class
        app = Application()
        # Start the tkinter event loop
        app.mainloop()
    except Exception as e:
        # If an exception occurs during the execution of the application
        # Log the exception with a message indicating an error occurred during application execution
        logging.exception("An error occurred during application execution")
    finally:
        pass
if __name__ == "__main__":
    main()
