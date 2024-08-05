import sqlite3

print("dbrequests module loaded")  # Debug statement

def add_dish(meal_type: str, dish: str):
    conn = sqlite3.connect('dishes.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO dishes (meal_type, dish) VALUES (?, ?)', (meal_type, dish))
    
    conn.commit()
    conn.close()

def get_dishes(meal_type: str):
    conn = sqlite3.connect('dishes.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT dish FROM dishes WHERE meal_type = ?', (meal_type,))
    dishes = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return dishes