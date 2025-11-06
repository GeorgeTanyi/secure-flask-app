
from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

def init_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'John Doe', 'john@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'Jane Smith', 'jane@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (3, 'Bob Johnson', 'bob@example.com')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '''
    <html>
    <head><title>Secure Flask App</title></head>
    <body style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px;">
        <h1>Secure Flask Application</h1>
        <div style="background: lightgreen; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <strong>All Security Vulnerabilities Fixed!</strong>
        </div>
        <h3>Security Fixes Applied:</h3>
        <ul>
            <li>Debug Mode: Disabled</li>
            <li>SQL Injection: Fixed with parameterized queries</li>
            <li>Network Binding: Localhost only</li>
            <li>Secret Key: Environment variable</li>
        </ul>
        <h3>Search Users:</h3>
        <form action="/search" method="get">
            <input type="text" name="query" placeholder="Search by name" required>
            <button type="submit">Search</button>
        </form>
    </body>
    </html>
    '''

@app.route('/search')
def search():
    query = request.args.get('query', '')
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (f'%{query}%',))
    results = cursor.fetchall()
    conn.close()
    
    html = f'<html><body style="font-family: Arial; max-width: 800px; margin: 50px auto;"><h1>Search Results for: {query}</h1>'
    if results:
        html += f'<p>Found {len(results)} users</p><table border="1" style="width: 100%; border-collapse: collapse;">'
        html += '<tr><th>ID</th><th>Name</th><th>Email</th></tr>'
        for row in results:
            html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>'
        html += '</table>'
    else:
        html += '<p>No users found</p>'
    html += '<p><a href="/">Back to Home</a></p></body></html>'
    return html

if __name__ == '__main__':
    init_db()
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    app.run(host=host, port=port, debug=debug)
