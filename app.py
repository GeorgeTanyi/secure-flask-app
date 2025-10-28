from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Vulnerability 1: Hardcoded secret key (SAST will catch this)
app.secret_key = 'hardcoded-secret-key-12345'

# Vulnerability 2: SQL Injection vulnerability
@app.route('/')
def index():
    return '''
        <h1>Secure Flask Demo</h1>
        <form action="/search" method="get">
            <input type="text" name="query" placeholder="Search users">
            <button type="submit">Search</button>
        </form>
    '''

@app.route('/search')
def search():
    query = request.args.get('query', '')
    
    # Vulnerability 3: SQL Injection - using string formatting
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
    cursor.execute("INSERT INTO users VALUES (2, 'Bob')")
    
    # VULNERABLE: Direct string interpolation
    sql = f"SELECT * FROM users WHERE name LIKE '%{query}%'"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    return f'<h2>Results:</h2><pre>{results}</pre>'

# Vulnerability 4: Debug mode enabled in production
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
