"""
Main entry point for the Solar Mo Lang
Run this file to start the program.
"""
import sys
from ui import App

def main():
    # Initialize the Application
    app = App()
    
    # Optional: Setup global exception handling or logging here
    
    try:
        # Start the main event loop
        app.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down SCADA system...")
        app.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()
