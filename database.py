import sqlite3
import json
import os
import chardet

DB_PATH = r'C:\Users\muzam\OneDrive\Desktop\PROJECTS\project-recommend\data\projects.db'
JSON_PATH = r'C:\Users\muzam\OneDrive\Desktop\PROJECTS\project-recommend\data\projects.json'


def init_db():
    try:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create projects table
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
                tools TEXT,
                steps TEXT
            )
        ''')

        # Check if table is empty
        cursor.execute("SELECT COUNT(*) FROM projects")
        count = cursor.fetchone()[0]
        print(f"Projects table has {count} rows before seeding.")  # Debug

        if count == 0:
            # Try to seed from JSON
            if os.path.exists(JSON_PATH):
                try:
                    with open(JSON_PATH, 'r', encoding='utf-8') as f:
                        projects = json.load(f)
                    if not projects:
                        print("Warning: projects.json is empty. Using fallback project.")
                        projects = [{
                            "name_en": "Sample Project",
                            "name_ar": "مشروع عينة",
                            "description_en": "A simple app for testing.",
                            "description_ar": "تطبيق بسيط للاختبار.",
                            "complexity": 3,
                            "scalability": 4,
                            "practicality": 5,
                            "tools": ["Python", "Streamlit"],
                            "steps": ["Setup environment", "Build UI", "Test", "Deploy"]
                        }]

                    for p in projects:
                        cursor.execute('''
                            INSERT INTO projects (name_en, name_ar, description_en, description_ar, complexity, scalability, practicality, tools, steps)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            p.get('name_en', p.get('name', 'Unnamed Project')),
                            p.get('name_ar', ''),
                            p.get('description_en', p.get('description', '')),
                            p.get('description_ar', ''),
                            p.get('complexity', 5),
                            p.get('scalability', 5),
                            p.get('practicality', 5),
                            json.dumps(p.get('tools', [])),
                            json.dumps(p.get('steps', []))
                        ))
                    print(f"Seeded {len(projects)} projects from JSON.")  # Debug
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse projects.json - {e}. Using fallback project.")
                    # Insert a fallback project
                    cursor.execute('''
                        INSERT INTO projects (name_en, name_ar, description_en, description_ar, complexity, scalability, practicality, tools, steps)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        "Sample Project",
                        "مشروع عينة",
                        "A simple app for testing.",
                        "تطبيق بسيط للاختبار.",
                        3, 4, 5,
                        json.dumps(["Python", "Streamlit"]),
                        json.dumps(["Setup environment", "Build UI", "Test", "Deploy"])
                    ))
                    print("Seeded 1 fallback project.")
                except Exception as e:
                    print(f"Error seeding database: {e}")
            else:
                print("Error: projects.json not found. Creating fallback project.")
                # Insert a fallback project
                cursor.execute('''
                    INSERT INTO projects (name_en, name_ar, description_en, description_ar, complexity, scalability, practicality, tools, steps)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    "Sample Project",
                    "مشروع عينة",
                    "A simple app for testing.",
                    "تطبيق بسيط للاختبار.",
                    3, 4, 5,
                    json.dumps(["Python", "Streamlit"]),
                    json.dumps(["Setup environment", "Build UI", "Test", "Deploy"])
                ))
                print("Seeded 1 fallback project.")

        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()


def get_all_projects():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects")
        rows = cursor.fetchall()
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
        print(f"Retrieved {len(projects)} projects from database: {projects}")  # Debug
        return projects
    except Exception as e:
        print(f"Error retrieving projects: {e}")
        return []
    finally:
        conn.close()