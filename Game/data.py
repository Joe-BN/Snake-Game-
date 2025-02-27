# handles all the database interactions in the game
# (create read and update)

import sqlite3

DB_NAME = 'score.db'  # The SQLite database file

def create_database():
    """Create the SQLite database and a table for the high score if they don't already exist."""
    # Connect to the database. Creates the file if it don't exist.
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create a table called 'scores' if it does not exist.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            high_score INTEGER
        )
    ''')
    
    # Check if a row exists; if not, insert a default high score of 0.
    cursor.execute("SELECT COUNT(*) FROM scores")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO scores (high_score) VALUES (?)", (0,))
    
    conn.commit()
    conn.close()

# Read data
def get_high_score():
    """Read and return the current high score from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # We assume the high score is stored in the row with id = 1.(witch may need to change later)
    cursor.execute("SELECT high_score FROM scores WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    
    # If no row is found, return 0 (shouldn't happen due to table initialization)
    return row[0] if row else 0

# Update the value of the high score
def update_high_score(new_score):
    """Update the high score in the database if new_score is higher than the current high score."""
    current_high = get_high_score()
    
    if new_score > current_high:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE scores SET high_score = ? WHERE id = 1", (new_score,))
        conn.commit()
        conn.close()
        # print(f"New high score saved: {new_score}") 

        return True

    else:
        # print(f"Score {new_score} did not beat the current high score of {current_high}.")

        return False
    
def reset_score():
    update_high_score(0)


def main():
    # Step 1: Create the database and table if they don't exist.
    create_database()
    
    # Step 2: Read and display the current high score.
    current_score = get_high_score()
    print (current_score)
    
    # Step 3: Get a new score from the user.
    try:
        new_score = int(input("Enter your new score: "))
        # Step 4: Update the high score if applicable.
        update_high_score(new_score)

    except ValueError:
        print("Invalid input. Please enter an integer.")



def  initialize_db():
    create_database()


if __name__ == "__main__":
    main()