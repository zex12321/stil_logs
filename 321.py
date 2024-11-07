import sqlite3

def view_data(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logins_passwords_urls")
    rows = cursor.fetchall()

    for row in rows:
        print(f"Login: {row[1]}, Password: {row[2]}, Url: {row[3]}")

    conn.close()

if __name__ == "__main__":
    db_name = input("Введите имя вашей базы данных (например, 'mydatabase.db'): ")
    view_data(db_name)
