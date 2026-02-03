"""
Database schema definitions for the Recruitment CRM.
"""
import sqlite3
import bcrypt
from datetime import datetime
from config import DATABASE_PATH, DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_EMAIL
from utils.constants import ROLE_ADMIN


def create_tables(conn):
    """Create all database tables."""
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            role VARCHAR(20) NOT NULL CHECK(role IN ('admin', 'recruiter', 'viewer')),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Candidates table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            location VARCHAR(100),
            linkedin_url VARCHAR(255),
            current_role VARCHAR(100),
            current_company VARCHAR(100),
            years_of_experience INTEGER,
            skills TEXT,
            education VARCHAR(255),
            status VARCHAR(20) NOT NULL DEFAULT 'Applied'
                CHECK(status IN ('Applied', 'Screening', 'Interview', 'Offer', 'Hired', 'Rejected')),
            position_applied VARCHAR(100),
            recruiter_id INTEGER,
            source VARCHAR(50),
            salary_expectation VARCHAR(50),
            notice_period VARCHAR(50),
            resume_url VARCHAR(255),
            notes TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recruiter_id) REFERENCES users(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """)

    # Call history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS call_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            recruiter_id INTEGER NOT NULL,
            call_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            call_type VARCHAR(20) CHECK(call_type IN ('Phone', 'Video', 'In-Person', 'Email')),
            duration INTEGER,
            outcome VARCHAR(50),
            notes TEXT,
            next_action VARCHAR(255),
            next_action_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
            FOREIGN KEY (recruiter_id) REFERENCES users(id)
        )
    """)

    # Activity log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action_type VARCHAR(50) NOT NULL,
            entity_type VARCHAR(50),
            entity_id INTEGER,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()


def create_indexes(conn):
    """Create database indexes for performance."""
    cursor = conn.cursor()

    # Indexes for candidates
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_recruiter ON candidates(recruiter_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates(email)")

    # Indexes for call_history
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_call_history_candidate ON call_history(candidate_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_call_history_recruiter ON call_history(recruiter_id)")

    # Indexes for activity_log
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_activity_log_user ON activity_log(user_id)")

    conn.commit()


def seed_default_admin(conn):
    """Create default admin user if no users exist."""
    cursor = conn.cursor()

    # Check if any users exist
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        # Hash the default admin password
        password_hash = bcrypt.hashpw(DEFAULT_ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt())

        # Insert default admin user
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, full_name, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            DEFAULT_ADMIN_USERNAME,
            DEFAULT_ADMIN_EMAIL,
            password_hash.decode('utf-8'),
            "System Administrator",
            ROLE_ADMIN,
            True
        ))

        conn.commit()
        print(f"Default admin user created: {DEFAULT_ADMIN_USERNAME}")
        print(f"Default password: {DEFAULT_ADMIN_PASSWORD}")
        print("Please change the password after first login!")


def initialize_database():
    """Initialize the database with tables, indexes, and seed data."""
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))

        # Create all tables
        create_tables(conn)
        print("Database tables created successfully.")

        # Create indexes
        create_indexes(conn)
        print("Database indexes created successfully.")

        # Seed default admin user
        seed_default_admin(conn)

        conn.close()
        print("Database initialized successfully.")
        return True

    except Exception as e:
        print(f"Error initializing database: {e}")
        return False


if __name__ == "__main__":
    # Run initialization when script is executed directly
    initialize_database()
