import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL from env: {DATABASE_URL}") 

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn
#Login/Register
#TEAMS
#PROJECTS
#TEAM_MEMBERS
#TASKS
#TASK_ASSIGNMENT
#COMMENTS










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
    
    conn.commit()
    cursor.close()
    conn.close()

def retrieve_team(team_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.*, u.username as created_by_name
        FROM teams t
        JOIN users u ON t.created_by = u.id
        WHERE t.id = %s
        """,(team_id,))
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_all_teams(user_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.id, t.name, t.description, t.created_by, t.created_at
        FROM teams t 
        JOIN team_members tm ON t.id = tm.team_id
        WHERE tm.user_id = %s
                   
        """,(user_id,))
    
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
    SELECT p.*, t.name as team_name, u.username as created_by_name
    FROM projects p
    JOIN teams t ON p.team_id = t.id
    JOIN users u ON p.created_by = u.id
    WHERE p.id = %s""",(project_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row



def get_all_projects(team_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p.*, t.name as team_name, u.username as created_by_name
    FROM projects p
    JOIN teams t ON p.team_id = t.id
    JOIN users u ON p.created_by = u.id
    WHERE p.team_id = %s
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
        SELECT tm.user_id, tm.team_id, tm.role, tm.joined, u.username, u.email 
        FROM team_members tm
        JOIN users u ON tm.user_id = u.id
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






















#                                        TASKS
def create_tasks_table():
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
        id SERIAL PRIMARY KEY,
        project_id INTEGER,
        title VARCHAR(30),
        description TEXT,
        status VARCHAR(30) DEFAULT 'in_progress',
        priority VARCHAR(20) DEFAULT 'medium',
        due_date TIMESTAMP,
        created_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(project_id,title),
        CHECK (status IN ('todo', 'in_progress', 'done', 'blocked')),
        CHECK (priority IN ('low','medium','high','urgent')),
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT)
        """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_task(project_id, title, description, status, priority,due_date, created_by):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (project_id, title, description, status, priority, due_date, created_by) VALUES 
        (%s, %s, %s, %s, %s, %s, %s)""",(project_id, title, description, status, priority,due_date, created_by))
    
    conn.commit()
    cursor.close()
    conn.close()


def get_task(task_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.*,
        p.name as Project_name,
        u1.username as created_by_name
        FROM tasks t
        JOIN projects p ON t.project_id = p.id
        JOIN users u1 ON t.created_by = u1.id
        WHERE t.id = %s""",(task_id,))
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return row

def get_all_tasks(project_id, status=None, priority=None, assigned_to=None):
    conn = init_db()
    cursor = conn.cursor()
    
    query = """
        SELECT t.*,
        p.name as Project_name,
        u1.username as created_by_name
        FROM tasks t
        JOIN projects p ON t.project_id = p.id
        JOIN users u1 ON t.created_by = u1.id
        WHERE p.id = %s
    """
    
    params = [project_id]
    
    # Add filters dynamically
    if status:
        query += " AND t.status = %s"
        params.append(status)
    
    if priority:
        query += " AND t.priority = %s"
        params.append(priority)
    
    if assigned_to:
        query += """ AND EXISTS (
            SELECT 1 FROM task_assignments ta 
            WHERE ta.task_id = t.id AND ta.user_id = %s
        )"""
        params.append(assigned_to)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def update_taskdb(task_id, title, description, status, priority, due_date):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title = %s,description = %s, status = %s,priority = %s,due_date = %s
        WHERE id = %s""",(title, description, status, priority, due_date,task_id))
    
    conn.commit()
    cursor.close()
    conn.close()



def delete_task(task_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = %s""",(task_id,))
    conn.commit()
    cursor.close()
    conn.close()














#                                                  TASK_ASSIGNMENT
def create_task_asign_table():
    conn = init_db()
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_assignments(
        user_id INTEGER,
        task_id INTEGER,
        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, task_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
        )""")
    
    conn.commit()
    cursor.close()
    conn.close()


def assign_task(task_id, user_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO task_assignments (task_id,user_id) VALUES (%s,%s)""",(task_id,user_id))
    
    conn.commit()
    cursor.close()
    conn.close()


def unassign_task(task_id, user_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM task_assignments
        WHERE task_id = %s AND user_id = %s""",(task_id,user_id))
    
    conn.commit()

    cursor.close()
    conn.close()

def get_task_assignees(task_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ta.user_id, u.username
        FROM task_assignments ta
        JOIN users u ON ta.user_id = u.id
        WHERE ta.task_id = %s""",(task_id,))
    
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return rows


def is_user_assigned(task_id, user_id):
    """Check if user is assigned to task"""
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT EXISTS(
            SELECT 1 FROM task_assignments 
            WHERE task_id = %s AND user_id = %s
        )
    """, (task_id, user_id))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0]






#                                                  COMMENTS
def create_comment_table():
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            task_id INTEGER,
            comment TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            edited_at TIMESTAMP,
            is_edited BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
            FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL)
            """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_comment(task_id, comment, created_by):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO comments (task_id,comment,created_by) VALUES (%s,%s,%s)""",(task_id,comment,created_by))
    
    conn.commit()
    cursor.close()
    conn.close()

def get_comment(comment_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.*,t.title,u.username
        FROM comments c
        JOIN tasks t ON c.task_id = t.id
        LEFT JOIN users u ON c.created_by = u.id
        WHERE c.id = %s""",(comment_id,))
    
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row

def get_task_comments(task_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.*,t.title,u.username
        FROM comments c
        JOIN tasks t ON c.task_id = t.id
        LEFT JOIN users u ON c.created_by = u.id
        WHERE c.task_id = %s
        """,(task_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def update_comment(comment_id, comment):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE comments
        SET comment = %s, edited_at = CURRENT_TIMESTAMP, is_edited = TRUE
        WHERE id = %s""",(comment,comment_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_comment(comment_id):
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM comments
        WHERE id = %s""",(comment_id,))
    
    conn.commit()
    cursor.close()
    conn.close()






def create_log_table():
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs(
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        action VARCHAR(50),
        entity_type VARCHAR(20),
        entity_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        details text,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL)
                   """)
    
    conn.commit()
    cursor.close()
    conn.close()

def insert_activity_log(user_id, action, entity_type, entity_id, details=None):
    conn = init_db()
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO activity_logs (user_id, action, entity_type, entity_id, details) 
        VALUES (%s, %s, %s, %s, %s)""",(user_id, action, entity_type, entity_id, details))
    
    conn.commit()
    cursor.close()
    conn.close()


    



if __name__ == "__main__":
    create_users_table()
    create_teams_table()
    create_projects_table()
    create_team_memeber_table()
    create_tasks_table()
    create_task_asign_table()
    create_comment_table()
    create_log_table()
    print("Created successfully!")

