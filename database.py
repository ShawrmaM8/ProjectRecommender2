import sqlite3
import json
import os

DB_PATH = 'data/projects.db'
JSON_PATH = 'data/projects.json'


def init_db():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            projects = json.load(f)
            # Continue with your logic to initialize the database using 'projects'
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except FileNotFoundError:
        print(f"File not found: {JSON_PATH}")
    except Exception as e:
        print(f"An error occurred: {e}")


    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT,
            name_ar TEXT,
            description_en TEXT,
            description_ar TEXT,
            complexity INTEGER,
            scalability INTEGER,
            practicality INTEGER,
            tools TEXT,  -- Stored as JSON string
            steps TEXT   -- Stored as JSON string
        )
    ''')

    # Seed from JSON if table is empty
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0 and os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r') as f:
            projects = json.load(f)
        for p in projects:
            cursor.execute('''
                INSERT INTO projects (name_en, name_ar, description_en, description_ar, complexity, scalability, practicality, tools, steps)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                p.get('name_en', p.get('name', '')),
                p.get('name_ar', ''),
                p.get('description_en', p.get('description', '')),
                p.get('description_ar', ''),
                p.get('complexity', 5),
                p.get('scalability', 5),
                p.get('practicality', 5),
                json.dumps(p.get('tools', [])),
                json.dumps(p.get('steps', []))
            ))
    conn.commit()
    conn.close()


def get_all_projects():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    rows = cursor.fetchall()
    conn.close()
    projects = []
    for r in rows:
        projects.append({
            'id': r[0],
            'name_en': r[1],
            'name_ar': r[2],
            'description_en': r[3],
            'description_ar': r[4],
            'complexity': r[5],
            'scalability': r[6],
            'practicality': r[7],
            'tools': json.loads(r[8]) if r[8] else [],
            'steps': json.loads(r[9]) if r[9] else []
        })
    return projectss