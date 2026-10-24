from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import psycopg2
import time


DB_CONFIG = {
    "host": "my-postgres-db",
    "database": "postgres",
    "user": "postgres",
    "password": "mysecretpassword"
}

def init_db():
    """Функция для создания таблицы при старте приложения"""
    time.sleep(3)
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                done BOOLEAN DEFAULT FALSE
            );
        """)
        
        cursor.execute("SELECT COUNT(*) FROM tasks;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO tasks (title, done) VALUES ('Вернуться в темп. Этап 7-8', true);")
            
            
        conn.commit()
        cursor.close()
        conn.close()
        print("База данных успешно инициализирована, таблица готова!")
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        
   
class TodoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/tasks':
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute("SELECT id, title, done FROM tasks;")
                rows = cursor.fetchall()
                
                tasks = []
                for row in rows:
                    tasks.append({
                        "id": row[0],
                        "title": row[1],
                        "done": row[2]
                    })
                
                cursor.close()
                conn.close()    
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(tasks).encode('utf-8'))
           
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Ошибка базы данных: {e}".encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    init_db()
    server = HTTPServer(('0.0.0.0', 8000), TodoHandler)
    print("Приложение запущено на порту 8000...")
    server.serve_forever()
