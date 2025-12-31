import psycopg2
def init_db():
    conn = psycopg2.connect(
        host='localhost',
        database='taskdb',
        user='postgres',
        password='13579Asa'
        )
    
    return conn
    

def create_users_table():
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at timestamp DEFAULT CURRENT_TIMESTAMP)  
        """)
    
    conn.commit()
    cursor.close()
    conn.close()

def insert_user(username,email,password_hash):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username,email,password_hash) VALUES (%s,%s,%s)
        """,(username,email,password_hash))
    
    conn.commit()
    cursor.close()
    conn.close()

def getuser(username):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE username = %s""",(username,))
    
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return user


def create_teams_table():
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        description TEXT,
        created_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT
        )""")
    
    conn.commit()
    cursor.close()
    conn.close()


def insert_team(name, description, created_by):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO teams (name,description,created_by) VALUES (%s,%s,%s)
        """,(name,description,created_by))
    
    conn.commit()
    cursor.close()
    conn.close()

def retrieve_team(team_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM teams
        WHERE id = %s
        """,(team_id,))
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_all_teams():
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM teams""")
    
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return rows


def update_team(team_id, name, description):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE teams
        SET name = %s, description = %s
        WHERE id = %s
        """,(name,description,team_id))
    
    conn.commit()
    cursor.close()
    conn.close()


def delete_team(team_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM teams
        WHERE id = %s
        """,(team_id,))
    conn.commit()
    cursor.close()
    conn.close()



if __name__ == "__main__":
    create_users_table()
    create_teams_table()
    print("Created successfully!")

