import sqlite3

# Database connection setup
def get_db_connection():
    try:
        conn = sqlite3.connect('app_database.db')
        conn.row_factory = sqlite3.Row  # Allows access to columns by name
        conn.execute('PRAGMA foreign_keys = ON')  # Enforce foreign key constraints
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Create necessary tables
def create_tables():
    conn = get_db_connection()
    if not conn:
        return  # Early exit if connection fails

    try:
        # Users table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL,  -- Admin, Trainer, Employee
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Question bank table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS question_bank (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trainer_id INTEGER,
                technology TEXT NOT NULL,
                topic TEXT NOT NULL,
                num_questions INTEGER,
                difficulty_level TEXT,  -- Easy, Medium, Hard
                questions TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trainer_id) REFERENCES users(id)
            )
        ''')

        # Curriculum table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS curriculum (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trainer_id INTEGER,
                technology TEXT NOT NULL,
                curriculum_file BLOB NOT NULL,  -- Storing binary data
                uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trainer_id) REFERENCES users(id)
            )
        ''')

        # Feedback table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                feedback_type TEXT NOT NULL,
                feedback_text TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Learning plans table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS learning_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                technology TEXT NOT NULL,
                areas_of_improvement TEXT NOT NULL,
                learning_goals TEXT NOT NULL,
                plan_details TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES users(id)
            )
        ''')

        # Assessment table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                question_bank_id INTEGER,
                score REAL,  -- Store as floating-point for precision
                completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES users(id),
                FOREIGN KEY (question_bank_id) REFERENCES question_bank(id)
            )
        ''')

        # Notifications table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                notification_text TEXT NOT NULL,
                is_read BOOLEAN DEFAULT FALSE,
                sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Issue resolution table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS issue_resolution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reported_by INTEGER,
                issue_description TEXT NOT NULL,
                resolution_status TEXT DEFAULT 'Pending',
                resolution_notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                resolved_at DATETIME,
                FOREIGN KEY (reported_by) REFERENCES users(id)
            )
        ''')

        conn.commit()
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        conn.close()
