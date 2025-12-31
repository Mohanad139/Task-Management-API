import psycopg2
def init_db():
    conn = psycopg2.connect(
        host='localhost',
        database='taskdb',
        user='postgres',
        password='13579Asa'
        )
    
    return conn
    
#                           USERS
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

#                           TEAMS
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
    
    team_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return team_id

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

def get_team_id(name):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM teams
        WHERE name = %s""",(name,))
    
    rows = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return rows


#                                        PROJECTS
def create_projects_table():
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        id SERIAL PRIMARY KEY,
        team_id INTEGER,
        name VARCHAR(100),
        description TEXT,
        created_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) DEFAULT 'active',
        CHECK(status IN ('active','completed','archived')),
        FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
        FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT
        )""")
    
    conn.commit()
    cursor.close()
    conn.close()

def insert_project(team_id, name, description, created_by, status):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO projects (team_id,name,description,created_by,status) VALUES (%s,%s,%s,%s,%s)
    """,(team_id,name,description,created_by,status))

    conn.commit()
    cursor.close()
    conn.close()


def retrieve_project(project_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * 
    FROM projects
    WHERE id = %s""",(project_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row



def get_all_projects(team_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM projects
    WHERE team_id = %s
    """,(team_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows



def update_project(project_id, name, description, status):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE projects
        SET name = %s , description = %s, status = %s
        WHERE id = %s
        """,(name,description,status,project_id))
    
    conn.commit()
    cursor.close()
    conn.close()

def delete_project(project_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM projects
        WHERE id = %s
        """,(project_id,))
    
    conn.commit()
    cursor.close()
    conn.close()



#                                        TEAMS_MEMEBR
def create_team_memeber_table():
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_members(
            user_id INTEGER,
            team_id INTEGER,
            role VARCHAR(20) DEFAULT 'member',
            joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(user_id,team_id),
            CHECK(role IN('owner','admin','member')),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE)
        """)
    
    conn.commit()
    cursor.close()
    conn.close()

def insert_member(user_id,team_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO team_members (user_id,team_id) VALUES (%s,%s)
        """,(user_id,team_id))
    
    conn.commit()
    cursor.close()
    conn.close()

def update_role(user_id,team_id,role):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE team_members 
        SET role = %s
        WHERE user_id = %s AND team_id = %s
        """,(role,user_id,team_id))
    
    conn.commit()
    cursor.close()
    conn.close()

def delete_member(user_id,team_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM team_members
        WHERE user_id = %s AND team_id = %s
        """,(user_id,team_id))
    
    conn.commit()
    cursor.close()
    conn.close()

def get_team_members(team_id):
    """Get all members of a team"""
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM team_members
        WHERE team_id = %s
    """, (team_id,))
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_user_role(user_id, team_id):
    """Get user's role in a specific team"""
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT role FROM team_members
        WHERE user_id = %s AND team_id = %s
    """, (user_id, team_id))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None




if __name__ == "__main__":
    create_users_table()
    create_teams_table()
    create_projects_table()
    create_team_memeber_table()
    print("Created successfully!")

