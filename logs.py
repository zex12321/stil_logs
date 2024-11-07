import os
import re
import sqlite3

def find_logins_passwords_and_urls(file_path):
    """Ищет логины, пароли и URL в указанном файле."""
    logins_passwords_urls = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

        # Обновленные регулярные выражения для USER, PASS и URL
        user_pattern = r'USER:\s*(?P<login>[^\s]+)'
        pass_pattern = r'PASS:\s*(?P<password>[^\n]+)'
        url_pattern = r'URL:\s*(?P<url>https?://[^\s]+)'

        # Шаблон для поиска USER, PASS и URL
        pattern = re.compile(rf'{user_pattern}.*?{pass_pattern}.*?{url_pattern}', re.DOTALL)

        # Находим все совпадения
        matches = pattern.finditer(content)
        for match in matches:
            login = match.group('login')
            password = match.group('password')
            url = match.group('url')
            logins_passwords_urls.append((login, password, url))
    
    return logins_passwords_urls

def process_log_files(directory):
    """Обрабатывает все текстовые файлы в указанной директории и ее поддиректориях."""
    logins_passwords_urls = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                logins_passwords_urls.extend(find_logins_passwords_and_urls(file_path))
    return logins_passwords_urls

def save_to_database(data, db_name):
    """Сохраняет данные в базу данных SQLite."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Создаем таблицу, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logins_passwords_urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        url TEXT NOT NULL
    )
    ''')

    # Вставка данных
    cursor.executemany('INSERT INTO logins_passwords_urls (login, password, url) VALUES (?, ?, ?)', data)
    
    conn.commit()
    conn.close()

def main(directory, db_name):
    # Обработка файлов для поиска логинов, паролей и URL
    logins_passwords_urls = process_log_files(directory)

    # Сохранение в базу данных
    if logins_passwords_urls:
        save_to_database(logins_passwords_urls, db_name)
        print(f"{len(logins_passwords_urls)} записей добавлены в базу данных.")
    else:
        print("Логины, пароли и URL не найдены.")

if __name__ == "__main__":
    directory_path = input("Введите путь к папке: ")
    database_name = input("Введите имя базы данных (например, 'mydatabase.db'): ")

    # Запуск основного процесса
    main(directory_path, database_name)