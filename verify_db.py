# verify_db.py
import sqlite3
import os

def verify_database():
    db_path = 'homework_marketplace.db'
    
    if not os.path.exists(db_path):
        print("ERROR: Database file not found!")
        return
    
    print(f"Database found: {os.path.abspath(db_path)}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✓ SUCCESS: 'user' table exists!")
            
            # Check table structure
            cursor.execute("PRAGMA table_info(user)")
            columns = cursor.fetchall()
            
            print("Table structure:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
                
            # Count rows (should be 0 initially)
            cursor.execute("SELECT COUNT(*) FROM user")
            count = cursor.fetchone()[0]
            print(f"Number of users in table: {count}")
            
        else:
            print("✗ ERROR: 'user' table does not exist!")
            
        conn.close()
        
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == '__main__':
    verify_database()
