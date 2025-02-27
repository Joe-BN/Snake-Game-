# handles all the database interactions in the game
# (create, read, and update)

import sqlite3
import sys
import os

# Determine the base path (dynamic path system)
if getattr(sys, 'frozen', False):
    # When bundled, place score.db beside the .exe
    base_path = os.path.dirname(sys.executable)
else:
    # When running from source, use the script's directory
    base_path = os.path.dirname(__file__)

# Define the database path
DB_NAME = os.path.join(base_path, 'score.db')

def create_database():
    """Create the SQLite database and a table for the high score if they don't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            high_score INTEGER
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM scores")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO scores (high_score) VALUES (?)", (0,))
    
    conn.commit()
    conn.close()

def get_high_score():
    """Read and return the current high score from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT high_score FROM scores WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    
    return row[0] if row else 0

def update_high_score(new_score):
    """Update the high score if new_score is higher than the current high score."""
    current_high = get_high_score()
    
    if new_score > current_high:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE scores SET high_score = ? WHERE id = 1", (new_score,))
        conn.commit()
        conn.close()
        return True
    else:
        return False

def reset_score():
    update_high_score(0)

def main():
    create_database()
    current_score = get_high_score()
    print(current_score)
    
    try:
        new_score = int(input("Enter your new score: "))
        update_high_score(new_score)
    except ValueError:
        print("Invalid input. Please enter an integer.")

def initialize_db():
    create_database()

if __name__ == "__main__":
    main()