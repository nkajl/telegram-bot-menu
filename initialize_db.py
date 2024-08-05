import sqlite3

def init_db():
    conn = sqlite3.connect('dishes.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_type TEXT NOT NULL,
            dish TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
